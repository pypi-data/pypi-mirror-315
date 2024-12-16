import asyncio
import json
import logging
import os
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import AsyncGenerator, Optional, Dict, Union, Generator, List

from huggingface_hub import hf_hub_download

from auralis.common.logging.logger import setup_logger, set_vllm_logging_level
from auralis.common.definitions.output import TTSOutput
from auralis.common.definitions.requests import TTSRequest
from auralis.common.metrics.performance import track_generation
from auralis.common.scheduling.two_phase_scheduler import TwoPhaseScheduler
from auralis.models.base import BaseAsyncTTSEngine, AudioOutputGenerator

class TTS:
    """A high-performance text-to-speech engine optimized for inference speed.

    This class provides an interface for both synchronous and asynchronous speech generation,
    with support for streaming output and parallel processing of multiple requests.
    """

    def __init__(self, scheduler_max_concurrency: int = 10, vllm_logging_level=logging.DEBUG):
        """Initialize the TTS engine.

        Args:
            scheduler_max_concurrency (int): Maximum number of concurrent requests to process.
            vllm_logging_level: Logging level for the VLLM backend.
        """
        set_vllm_logging_level(vllm_logging_level)

        self.scheduler: Optional[TwoPhaseScheduler] = TwoPhaseScheduler(scheduler_max_concurrency)
        self.tts_engine: Optional[BaseAsyncTTSEngine] = None
        self.concurrency = scheduler_max_concurrency
        self.max_vllm_memory: Optional[int] = None
        self.logger = setup_logger(__file__)
        self.loop = None

    def _ensure_event_loop(self):
        """Ensures that an event loop exists and is set."""
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

    def from_pretrained(self, model_name_or_path: str, **kwargs):
        """Load a pretrained model from local path or Hugging Face Hub.
           **THIS METHOD IS SYNCHRONOUS**

        Args:
            model_name_or_path (str): Local path or Hugging Face model identifier.
            **kwargs: Additional arguments passed to the model's from_pretrained method.

        Returns:
            TTS: The TTS instance with loaded model.

        Raises:
            ValueError: If the model cannot be loaded from the specified path.
        """
        from auralis.models.registry import MODEL_REGISTRY

        # Ensure an event loop exists for potential async operations within from_pretrained
        self._ensure_event_loop()

        try:
            with open(os.path.join(model_name_or_path, 'config.json'), 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            try:
                config_path = hf_hub_download(repo_id=model_name_or_path, filename='config.json')
                with open(config_path, 'r') as f:
                    config = json.load(f)
            except Exception as e:
                raise ValueError(f"Could not load model from {model_name_or_path} neither locally or online: {e}")

        # Run potential async operations within from_pretrained in the event loop
        async def _load_model():
            return MODEL_REGISTRY[config['model_type']].from_pretrained(model_name_or_path, **kwargs)

        self.tts_engine = self.loop.run_until_complete(_load_model()) # to start form the correct loop

        return self

    async def prepare_for_streaming_generation(self, request: TTSRequest):
        """Prepare conditioning for streaming generation.

        Args:
            request (TTSRequest): The TTS request containing speaker files.

        Returns:
            Partial function with prepared conditioning for generation.
        """
        conditioning_config = self.tts_engine.conditioning_config
        if conditioning_config.speaker_embeddings or conditioning_config.gpt_like_decoder_conditioning:
            gpt_cond_latent, speaker_embeddings = await self.tts_engine.get_audio_conditioning(request.speaker_files)
            return partial(self.tts_engine.get_generation_context,
                           gpt_cond_latent=gpt_cond_latent,
                           speaker_embeddings=speaker_embeddings)

    async def _prepare_generation_context(self, input_request: TTSRequest):
        """Prepare the generation context for the first phase of speech synthesis.

        Args:
            input_request (TTSRequest): The TTS request to process.

        Returns:
            dict: Dictionary containing parallel inputs and the original request.
        """
        conditioning_config = self.tts_engine.conditioning_config
        input_request.start_time = time.time()
        if input_request.context_partial_function:
            (audio_token_generators, requests_ids,
             speaker_embeddings,
             gpt_like_decoder_conditioning) = \
                await input_request.context_partial_function(input_request)
        else:
            audio_token_generators, speaker_embeddings, gpt_like_decoder_conditioning = None, None, None

            if conditioning_config.speaker_embeddings and conditioning_config.gpt_like_decoder_conditioning:
                (audio_token_generators, requests_ids,
                 speaker_embeddings,
                 gpt_like_decoder_conditioning) = await self.tts_engine.get_generation_context(input_request)
            elif conditioning_config.speaker_embeddings:
                (audio_token_generators, requests_ids,
                 speaker_embeddings) = await self.tts_engine.get_generation_context(input_request)
            elif conditioning_config.gpt_like_decoder_conditioning:
                (audio_token_generators, requests_ids,
                 gpt_like_decoder_conditioning) = await self.tts_engine.get_generation_context(input_request)
            else:
                audio_token_generators, requests_ids = await self.tts_engine.get_generation_context(input_request)

        parallel_inputs = [
            {
                'generator': gen,
                'speaker_embedding': speaker_embeddings[i] if
                speaker_embeddings is not None and isinstance(speaker_embeddings, list) else
                speaker_embeddings if speaker_embeddings is not None else
                None,
                'multimodal_data': gpt_like_decoder_conditioning[i] if
                gpt_like_decoder_conditioning is not None and isinstance(gpt_like_decoder_conditioning, list) else
                gpt_like_decoder_conditioning if gpt_like_decoder_conditioning is not None else
                None,
                'request': input_request,
            }
            for i, gen in enumerate(audio_token_generators)
        ]

        return {
            'parallel_inputs': parallel_inputs,
            'request': input_request
        }

    async def _process_single_generator(self, gen_input: Dict) -> AudioOutputGenerator:
        """Process a single generator to produce speech output.

        Args:
            gen_input (Dict): Dictionary containing generator and conditioning information.

        Returns:
            AudioOutputGenerator: Generator yielding audio chunks.

        Raises:
            Exception: If any error occurs during processing.
        """
        try:
            async for chunk in self.tts_engine.process_tokens_to_speech(  # type: ignore
                    generator=gen_input['generator'],
                    speaker_embeddings=gen_input['speaker_embedding'],
                    multimodal_data=gen_input['multimodal_data'],
                    request=gen_input['request'],
            ):
                yield chunk
        except Exception as e:
            raise e

    @track_generation
    async def _second_phase_fn(self, gen_input: Dict) -> AudioOutputGenerator:
        """Second phase of speech generation: Convert tokens to speech.

        Args:
            gen_input (Dict): Dictionary containing generator and conditioning information.

        Returns:
            AudioOutputGenerator: Generator yielding audio chunks.
        """
        async for chunk in self._process_single_generator(gen_input):
            yield chunk

    async def generate_speech_async(self, request: TTSRequest) -> Union[AsyncGenerator[TTSOutput, None], TTSOutput]:
        """Generate speech asynchronously from text.

        Args:
            request (TTSRequest): The TTS request to process.

        Returns:
            Union[AsyncGenerator[TTSOutput, None], TTSOutput]: Audio output, either streamed or complete.

        Raises:
            RuntimeError: If instance was not created for async generation.
        """
        self._ensure_event_loop()

        async def process_chunks():
            chunks = []
            try:
                async for chunk in self.scheduler.run(
                        inputs=request,
                        request_id=request.request_id,
                        first_phase_fn=self._prepare_generation_context,
                        second_phase_fn=self._second_phase_fn
                ):
                    if request.stream:
                        yield chunk
                    chunks.append(chunk)
            except Exception as e:
                self.logger.error(f"Error during speech generation: {e}")
                raise

            if not request.stream:
                yield TTSOutput.combine_outputs(chunks)

        if request.stream:
            return process_chunks()
        else:
            async for result in process_chunks():
                return result

    @staticmethod
    def split_requests(request: TTSRequest, max_length: int = 100000) -> List[TTSRequest]:
        """Split a long text request into multiple smaller requests.

        Args:
            request (TTSRequest): The original TTS request.
            max_length (int): Maximum length of text per request.

        Returns:
            List[TTSRequest]: List of split requests.
        """
        if len(request.text) <= max_length:
            return [request]

        text_chunks = [request.text[i:i + max_length]
                       for i in range(0, len(request.text), max_length)]

        return [
            (copy := request.copy(), setattr(copy, 'text', chunk), setattr(copy, 'request_id', uuid.uuid4().hex))[0]
            for chunk in text_chunks
        ]

    async def _process_multiple_requests(self, requests: List[TTSRequest], results: Optional[List] = None) -> Optional[
        TTSOutput]:
        """Process multiple TTS requests in parallel.

        Args:
            requests (List[TTSRequest]): List of requests to process.
            results (Optional[List]): Optional list to store results for streaming.

        Returns:
            Optional[TTSOutput]: Combined audio output if not streaming, None otherwise.
        """
        output_queues = [asyncio.Queue() for _ in requests] if results is not None else None

        async def process_subrequest(idx, sub_request, queue: Optional[asyncio.Queue] = None):
            chunks = []
            async for chunk in self.scheduler.run(
                    inputs=sub_request,
                    request_id=sub_request.request_id,
                    first_phase_fn=self._prepare_generation_context,
                    second_phase_fn=self._second_phase_fn
            ):
                chunks.append(chunk)
                if queue is not None:
                    await queue.put(chunk)

            if queue is not None:
                await queue.put(None)
            return chunks

        tasks = [
            asyncio.create_task(
                process_subrequest(
                    idx,
                    sub_request,
                    output_queues[idx] if output_queues else None
                )
            )
            for idx, sub_request in enumerate(requests)
        ]

        if results is not None:
            for idx, queue in enumerate(output_queues):
                while True:
                    chunk = await queue.get()
                    if chunk is None:
                        break
                    results[idx].append(chunk)
            return None
        else:
            all_chunks = await asyncio.gather(*tasks)
            complete_audio = [chunk for chunks in all_chunks for chunk in chunks]
            return TTSOutput.combine_outputs(complete_audio)

    def generate_speech(self, request: TTSRequest) -> Union[Generator[TTSOutput, None, None], TTSOutput]:
        """Generate speech synchronously from text.

        Args:
            request (TTSRequest): The TTS request to process.

        Returns:
            Union[Generator[TTSOutput, None, None], TTSOutput]: Audio output, either streamed or complete.

        Raises:
            RuntimeError: If instance was created for async generation.
        """
        self._ensure_event_loop()
        requests = self.split_requests(request)

        if request.stream:
            # Streaming case
            def streaming_wrapper():
                for sub_request in requests:
                    # For streaming, execute the async gen
                    async def process_stream():
                        try:
                            async for chunk in self.scheduler.run(
                                    inputs=sub_request,
                                    request_id=sub_request.request_id,
                                    first_phase_fn=self._prepare_generation_context,
                                    second_phase_fn=self._second_phase_fn
                            ):
                                yield chunk
                        except Exception as e:
                            self.logger.error(f"Error during streaming: {e}")
                            raise

                    # Execute the async gen
                    generator = process_stream()
                    try:
                        while True:
                            chunk = self.loop.run_until_complete(anext(generator))
                            yield chunk
                    except StopAsyncIteration:
                        pass

            return streaming_wrapper()
        else:
            # Non streaming
            return self.loop.run_until_complete(self._process_multiple_requests(requests))

    async def shutdown(self):
        """Shuts down the TTS engine and scheduler."""
        if self.scheduler:
            await self.scheduler.shutdown()
        if self.tts_engine and hasattr(self.tts_engine, 'shutdown'):
            await self.tts_engine.shutdown()