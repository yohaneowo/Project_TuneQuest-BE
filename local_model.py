import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import torch
import random
# user_prompt: str|None, user_melody: str|None
def generate_musicByLocal():
    print(torch.__version__)
    print(torch.version.cuda)
    model = MusicGen.get_pretrained('facebook/musicgen-melody')
    model.set_generation_params(duration=1)  # generate 8 seconds.
    descriptions = ['happy rock in modern style with electric guitar and drums']
    melody, sr = torchaudio.load('./bach.mp3')
    # generates using the melody from the given audio and the provided descriptions.
    wav = model.generate_with_chroma(descriptions, melody[None].expand(1, -1, -1), sr,True)
    for idx, one_wav in enumerate(wav):
        # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
        audio_write(f'{random.randint(1,100)}', one_wav.cpu(), model.sample_rate, strategy="loudness")
        return 'done'
