import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import random
import replicate

class Musicgen:
    def __init__(self, top_k: int, top_p: int, prompt: str, duration: int, temperature: int, continuation: bool, model_version: str, output_format: str, continuation_start: int, multi_band_diffusion: bool, normalization_strategy: str, classifier_free_guidance: int,  generate_method: str , audiofile_path: str, mission_id: str):
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
        self.generate_method = generate_method
        self.audiofile_path = audiofile_path
        self.mission_id = mission_id

    def generate_music(self):
        if self.generate_method == 'replicate':
            self.generate_music_by_replicate()
        if self.generate_method == 'local':
            self.generate_music_by_local()

    def generate_music_by_replicate(self):
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

    def generate_music_by_local(self):
        audiofile_path = self.audiofile_path
        model = MusicGen.get_pretrained('facebook/musicgen-melody')
        model.set_generation_params(
            top_k=self.top_k,
            top_p=self.top_p,
            temperature=self.temperature,
            duration=self.duration,
            cfg_coef=self.classifier_free_guidance,
        )  # generate 8 seconds.

        descriptions = self.prompt
        melody, sr = torchaudio.load(self.audiofile_path)
        # generates using the melody from the given audio and the provided descriptions.
        wav = model.generate_with_chroma(descriptions, melody[None].expand(1, -1, -1), sr, True)

        # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
        audio_write(f'{self.mission_id}', wav.cpu(), model.sample_rate, strategy="loudness")


