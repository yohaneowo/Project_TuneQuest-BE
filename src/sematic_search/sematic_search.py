import pymongo
from src.sematic_search.generate_embedding import generate_embedding
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
client = pymongo.MongoClient(os.getenv("MONGO_URL"))
db = client.mydatabase
collection = db.embedded_music

def semantic_search_by_name(query):
  results = collection.aggregate([
    {"$vectorSearch": {
      "queryVector": asyncio.run(generate_embedding(query)),
      "path": "embedded_name",
      "numCandidates": 100,
      "limit": 5,
      "index": "name_vector_index",
        }
    }, {
      '$project': {
        '_id': 0, 
        'name': 1, 
        'genres': 1, 
        'prompt': 1, 
        'score': {
          '$meta': 'vectorSearchScore'
        }
      }
    }
  ])
  return results

def semantic_search_by_prompt(query):
  results = collection.aggregate([
    {"$vectorSearch": {
      "queryVector": asyncio.run(generate_embedding(query)),
      "path": "embedded_prompt",
      "numCandidates": 100,
      "limit": 5,
      "index": "embedded_prompt_vector_index",
        }
    }, {
      '$project': {
        '_id': 0, 
        'name': 1, 
        'genres': 1, 
        'prompt': 1, 
        'score': {
          '$meta': 'vectorSearchScore'
        }
      }
    }
  ])
  return results

# results = semantic_search_by_name("cool")

# # print(type(results))

# for embedded_music in results:
#     print(embedded_music)
#     # print(f'Music Name: {embedded_music["name"]},\nGenre: {embedded_music["genre"]}\nPrompt: {embedded_music["prompt"]}\n')