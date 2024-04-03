import httpx
import os
import soundfile as sf
import torchopenl3
import torch.nn.functional as F
from pathlib import Path


async def hf_embedding(text: str) -> list[float]:
    huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
    embedding_url = os.getenv("EMBEDDING_URL")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            embedding_url,
            headers={"Authorization": f"Bearer {huggingface_token}"},
            json={"inputs": text})

    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

    return response.json()


def audio_embedding(file_path: str) -> list[float]:
    path = Path(file_path)

    audio, sr = sf.read(path)

    # 計算所需的樣本數（假設音訊的取樣率是sr）
    num_samples = 3 * sr

    # 如果音訊長度小於3秒，則使用整個音訊；否則，截取前3秒
    audio_segment = audio[:num_samples] if len(audio) > num_samples else audio
    emb, ts = torchopenl3.get_audio_embedding(audio_segment, sr, embedding_size=512)

    # 将嵌入向量扁平化
    flat_emb = emb.view(-1)

    # 使用平均池化调整emb的长度到2048
    # 注意：adaptive_avg_pool1d 需要输入为3D tensor，我们需要在前面添加一个维度，然后再去除
    flat_emb = flat_emb.unsqueeze(0)  # 添加维度，变为[1, N]
    pooled_emb = F.adaptive_avg_pool1d(flat_emb, 2048)  # 平均池化到2048
    pooled_emb = pooled_emb.squeeze(0)  # 去除维度，回到[2048]

    emb_list = pooled_emb.tolist()

    return emb_list


if __name__ == "__main__":
    list = audio_embedding("./sample/tmpyze0b569.wav")
    print(list)