
import os
from fastapi import  HTTPException, File, UploadFile,APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, FilePath, validator, json
from bson import ObjectId
from typing import Optional, List
from datetime import datetime, timezone
from src.sematic_search.generate_embedding import hf_embedding, audio_embedding
from src.sematic_search.sematic_search import keyword_search as kwdsearch, semantic_search_by_prompt as ssearch_prompt, semantic_search_by_audio as ssearch_audio
from pathlib import Path
from enum import unique, Enum
import uuid
import aiofiles
import aiofiles.os



router = APIRouter(
    prefix='/sematic_search',
    tags=['sematic_search']
)


# MongoDB connection URL
MONGO_URL = os.getenv("MONGO_URL") # MongoDB connection URL
client = AsyncIOMotorClient(MONGO_URL)
database = client["mydatabase"]
collection = database["embedded_music"]

# Define an Enumeration for music genre checking

@unique

class GenreEnum(str, Enum):
    blues = 'Blues'
    classical = 'Classical'
    country = 'County'
    disco = 'Disco'
    hiphop = 'Hip-hop'
    jazz = 'Jazz'
    metal = 'Metal'
    pop = 'Pop'
    reggae = 'Reggae'
    rock = 'Rock'
class GeneratedMusic(BaseModel):
    name: str = Field(examples=["Midnight Jazz Escape"])
    genre: Optional[GenreEnum] = Field(default=None, examples=["Jazz"])
    prompt: str = Field(examples=["Late night jazz with a melancholic piano and a double bass groove"])
    user_id: int = Field(examples=[123])
    created_at: datetime

    # 兼容windows(.\\docs\\file.txt)或是unix(./docs/file.txt)的路徑寫法
    store_path: FilePath = Field(examples=["./sample/tmpte4m9jx6.wav"])
    embedded_prompt: Optional[List[float]] = Field(default=None)
    embedded_audio: Optional[List[float]] = Field(default=None)

    # Validator to ensure genre is one of the specified options or null
    @validator('genre', pre=True, always=True)
    def check_genre(cls, v):
        if v is None or v in GenreEnum.__members__.values():
            return v
        raise ValueError(f'Genre must be one of {list(GenreEnum)} or null')


@router.post("/items/", response_model=GeneratedMusic)
async def create_item(item: GeneratedMusic):
    item.embedded_prompt = await hf_embedding(item.prompt)
    item.created_at = datetime.now(timezone.utc)

    # 兼容windows(.\\docs\\file.txt)或是unix(./docs/file.txt)的路徑寫法
    path = Path(item.store_path)
    item.embedded_audio = audio_embedding(str(path))

    # 不論輸入windows(.\\docs\\file.txt)或是unix(./docs/file.txt)的路徑寫法，最後都會轉成unix的寫法儲存
    item.store_path = str(path.as_posix())
    await collection.insert_one(item.model_dump())
    return item


@router.get("/items/id/{id}", response_model=GeneratedMusic)
async def search_by_id(id: str):
    item = await collection.find_one({"_id": ObjectId(id)})
    if item:
        return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/items/{name_or_prompt}")
def keyword_search_by_name_or_prompt(name_or_prompt: str, limit: Optional[int] = 10):
    items = kwdsearch(name_or_prompt, limit=limit)
    if items:
        return list(items)
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/items/prompt/semantic/{prompt}")
def semantic_search_by_prompt(prompt: str, limit: Optional[int] = 10):
    items = ssearch_prompt(prompt, limit=limit)
    if items:
        return list(items)
    raise HTTPException(status_code=404, detail="Item not found")


@router.put("/items/{id}", response_model=GeneratedMusic)
async def update_item(id: str, item: GeneratedMusic):
    updated_item = await collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": item.model_dump()}
    )
    if updated_item:
        return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/items/{id}", response_model=GeneratedMusic)
async def delete_item(id: str):
    deleted_item = await collection.find_one_and_delete({"_id": ObjectId(id)})
    if deleted_item:
        return deleted_item
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/audio_search")
async def audio_search(file: UploadFile = File(...), limit: Optional[int] = 10):
    contents = await file.read()
    uid = uuid.uuid4()
    temp_file_path = f"temp_file_{uid}"
    async with aiofiles.open(temp_file_path, "wb") as temp_file:  # Use aiofiles for async file operations
        await temp_file.write(contents)

    try:
        items = ssearch_audio(temp_file_path,
                              limit)  # Ensure this can work with async or consider making the call synchronous if it must be
        return list(items)
    finally:
        await aiofiles.os.remove(temp_file_path)  # Use aiofiles for async file removal

