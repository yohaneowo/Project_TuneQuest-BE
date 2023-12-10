from audiocraft.data.audio import audio_write
import torch
print(torch.__version__)
print(torch.version.cuda)
model = MusicGen.get_pretrained('facebook/musicgen-stereo-melody-large')
model.set_generation_params(duration=30)  # generate 8 seconds.

descriptions = ['happy rock in modern style with electric guitar and drums']

melody, sr = torchaudio.load('./bach.mp3')
# generates using the melody from the given audio and the provided descriptions.
wav = model.generate_with_chroma(descriptions, melody[None].expand(1, -1, -1), sr)

for idx, one_wav in enumerate(wav):
    # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
    audio_write(f'{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness")

