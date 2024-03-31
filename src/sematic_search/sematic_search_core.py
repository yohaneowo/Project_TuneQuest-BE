from fastapi import FastAPI, HTTPException,APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from bson import ObjectId
from typing import Optional, List
from src.sematic_search.generate_embedding import generate_embedding
from src.sematic_search.sematic_search import semantic_search_by_prompt as ss_by_prompt, semantic_search_by_name as ss_by_name
import uvicorn
import os

router = APIRouter(
    prefix='/sematic_search',
    tags=['sematic_search']
)


# MongoDB connection URL
MONGO_URL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
database = client["mydatabase"]
collection = database["embedded_music"]


class GeneratedMusic(BaseModel):
    name: Optional[str] = Field(default=None, examples=["A cool music I just created"])
    genre: Optional[str] = Field(default=None, examples=["Rock"])
    prompt: str = Field(default=None, examples=["90s rock song with electric guitar and heavy drums"])
    embedded_name: Optional[List[float]] = Field(default=None)
    embedded_prompt: Optional[List[float]] = Field(default=None)


@router.post("/items/", response_model=GeneratedMusic)
async def create_item(item: GeneratedMusic):
    item.embedded_name = await generate_embedding(item.name)
    item.embedded_prompt = await generate_embedding(item.prompt)
    await collection.insert_one(item.model_dump())
    return item


@router.get("/items/{id}", response_model=GeneratedMusic)
async def read_item(id: str):
    item = await collection.find_one({"_id": ObjectId(id)})
    if item:
        return item
    raise HTTPException(status_code=404, detail="Item not found")



# # 關鍵字搜尋，建議不要用(非原始用途)
# @router.get("/items/name/{name}", response_model=List[GeneratedMusic])
# async def read_items_by_name(name: str):
#     cursor = collection.find({"name": {'$regex':name}}).limit(5)
#     items = await cursor.to_list(length=None)
#     if items:
#         return items
#     raise HTTPException(status_code=404, detail="Item not found")


@router.get("/ssearch/name/{name}", response_model=List[GeneratedMusic])
def semantic_search_by_name(name: str):
    items = ss_by_name(name)
    if items:
        return items
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/ssearch/prompt/{prompt}", response_model=List[GeneratedMusic])
def semantic_search_by_prompt(prompt: str):
    items = ss_by_prompt(prompt)
    if items:
        return items
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

if __name__ == "__main__":
    uvicorn.run(router, log_level="info")