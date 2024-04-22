import pymongo
from src.prompt_assistant.generate_embedding import hf_embedding
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
client = pymongo.MongoClient(os.getenv("MONGO_URL"))
db = client.mydatabase
collection = db.embedded_music

def semantic_search_by_prompt(query, limit = 10):
  results = collection.aggregate([
    {
      "$vectorSearch": {
        "queryVector": asyncio.run(hf_embedding(query)),
        "path": "embedded_prompt",
        "numCandidates": 100,
        "limit": limit, # Control how many you result you want to get.
        "index": "embedded_prompt_vector_index",
      }
    },
    {
      "$project": {
        "_id": 0,
        "name": 1,
        "genre": 1,
        "prompt": 1,
        "user_id": 1,
        "created_at": 1,
        "store_path": 1,
        "score": {
          "$meta": "vectorSearchScore"
        }
      }
    },
    {
      "$match": {
        "score": {
          "$gte": 0.5 # filter out any reslut that below 0.5 vectorSearchScore.
        }
      }
    }
  ])
  return results