import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from src.music_genre_classification.classification_core import predict_genre
from src.sematic_search.sematic_search_core import create_item as create_sematic_search_item , GeneratedMusic
from fastapi import UploadFile, File
import random
import replicate
import requests
import uuid
import os
import io
from urllib import request, parse
import mimetypes
from datetime import datetime

class Musicgen:
    def __init__(self, generate_method:str ,top_k: float, top_p: float, prompt: str, duration: int, temperature: float, continuation: bool, model_version: str, output_format: str, continuation_start: int, multi_band_diffusion: bool, normalization_strategy: str, classifier_free_guidance: int, audiofile_path: str, mission_id: str):
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
        self.generate_method = generate_method

    def generate_music(self):
        if self.generate_method == 'replicate':
            return self.generate_music_by_replicate()
        if self.generate_method == 'local':
            return self.generate_music_by_local()

    def generate_music_by_replicate(self):
        mv = ""
        if self.model_version == 'facebook/musicgen-melody':
                mv = "melody-large"
        output = replicate.run(
            "meta/musicgen:7be0f12c54a8d033a0fbd14418c9af98962da9a86f5ff7811f9b3423a1f0b7d7",
            input={
                # "top_k": self.top_k,
                # "top_p": self.top_p,
                "prompt": self.prompt,
                "duration": self.duration,
                # "temperature": self.temperature,
                # "model_version": mv,
                # "output_format": self.output_format,
                # "multi_band_diffusion": self.multi_band_diffusion,
                # "normalization_strategy": self.normalization_strategy,
                # "classifier_free_guidance": self.classifier_free_guidance

            }
        )
        print(output)
        unique_id = uuid.uuid4()
        file_name = f"{self.prompt}_{unique_id}.wav"
        # folder_path = "./music_storage/"
        folder_path = os.path.join(os.getcwd(), "music_storage")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, file_name)
        response = requests.get(output)
        if response.status_code == 200:
            # 将文件内容写入本地文件
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print("文件下载成功！")
        else:
            print("下载失败，状态码：", response.status_code)

        # DUMMY data
        # genre = "Jazz"
        # self.prompt = "sad jazz"
        # folder_path = os.path.join(os.getcwd(), "music_storage")
        # file_name1 = "sad jazz_86958c14-43ef-4d2e-81b7-166e0d00d594.wav"
        # file_name2 = "sad jazz_c470b51d-f2da-4ff5-ac96-012676a10e84.wav"
        # file_name = "sad jazz_c6675dcf-2b3d-4c48-a624-9cbed425f0bf.wav"
        # file_name = "sad jazz_d454863d-ab8e-4b10-a1c8-320bd540893c.wav"
        # file_name = "sad piano jazz_9b4a78de-c5c3-49cd-bcff-c4d8f9ea6bb3.wav"
        # file_name = "sad piano_c4e03c78-b1ea-44b0-90cb-f0e98dde07ee.wav"
        # file_path = os.path.join(folder_path, file_name)
        # print(file_path)

        final_result = {
            "prompt": self.prompt,
            "duration": self.duration,
            "audiofile_path": file_path,
            "audiofile_name": file_name,
        }
        return final_result
        # 测试路径用
        # file_name = "example_test.txt"
        # full_path = os.path.join(folder_path, file_name)
        #
        # # Ensure the directory exists, and create it if it doesn't
        # if not os.path.exists(folder_path):
        #     os.makedirs(folder_path)
        #
        # # Open (or create) the text file and write some content
        # with open(full_path, 'w') as file:
        #     file.write("Hello, world!")
        #
        # print(f"File '{file_name}' has been created in '{folder_path}' with some content.")
        #



    def generate_music_by_local(self):
        audiofile_path = self.audiofile_path
        model = MusicGen.get_pretrained('facebook/musicgen-melody')
        # 解决必须输入list的笨蛋方案
        fixed_list_for_desc = [self.prompt]
        model.set_generation_params(
            top_k=self.top_k,
            top_p=self.top_p,
            temperature=self.temperature,
            duration=self.duration,
            cfg_coef=self.classifier_free_guidance,
        )  # generate 8 seconds.

        descriptions = fixed_list_for_desc
        melody, sr = torchaudio.load(self.audiofile_path)
        # generates using the melody from the given audio and the provided descriptions.
        wav = model.generate_with_chroma(descriptions, melody[None].expand(1, -1, -1), sr, True)
        # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
        for idx, one_wav in enumerate(wav):
            audio_write(f'{self.mission_id}', one_wav.cpu(), model.sample_rate, strategy="loudness")



