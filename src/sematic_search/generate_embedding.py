import httpx
import os

async def generate_embedding(text: str) -> list[float]:
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
