import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

model = MusicGen.get_pretrained('facebook/musicgen-melody')
model.set_generation_params(duration=1)  # generate 8 seconds.

descriptions = ['sad jazz']

melody, sr = torchaudio.load('./bach.mp3')
# generates using the melody from the given audio and the provided descriptions.
wav = model.generate_with_chroma(descriptions, melody[None].expand(1, -1, -1), sr)

for idx, one_wav in enumerate(wav):
    # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
    audio_write(f'{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness")