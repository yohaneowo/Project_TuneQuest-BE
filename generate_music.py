import replicate
import celery as celery
class MusicGenerationInput:
    def __init__(self, top_k: int, top_p: int, prompt: str, duration: int, temperature: int, continuation: bool, model_version: str, output_format: str, continuation_start: int, multi_band_diffusion: bool, normalization_strategy: str, classifier_free_guidance: int):
        self.top_k = top_k
        self.top_p = top_p
        self.prompt = prompt
        self.duration = duration
        self.temperature = temperature
        self.continuation = continuation
        self.model_version = model_version
        self.output_format = output_format
        self.continuation_start = continuation_start
        self.multi_band_diffusion = multi_band_diffusion
        self.normalization_strategy = normalization_strategy
        self.classifier_free_guidance = classifier_free_guidance


async def generate_music_by_replicate (self: MusicGenerationInput):
    output = replicate.run(
        "meta/musicgen:7be0f12c54a8d033a0fbd14418c9af98962da9a86f5ff7811f9b3423a1f0b7d7",
        input={
            "top_k": self.top_k,
            "top_p": self.top_p,
            "prompt": self.prompt,
            "duration": self.duration,
            "temperature": self.temperature,
            "continuation": self.continuation,
            "model_version": self.model_version,
            "output_format": self.output_format,
            "continuation_start": self.continuation_start,
            "multi_band_diffusion": self.multi_band_diffusion,
            "normalization_strategy": self.normalization_strategy,
            "classifier_free_guidance": self.classifier_free_guidance

        }
    )
    print(output)

async def generate_music_by_local():
    pass