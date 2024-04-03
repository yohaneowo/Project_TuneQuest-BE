import pymongo
from src.sematic_search.generate_embedding import hf_embedding, audio_embedding
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
client = pymongo.MongoClient(os.getenv("MONGO_URL"))
db = client.mydatabase
collection = db.embedded_music

def keyword_search(query, limit = 10):
  results = collection.aggregate([
      {
        "$search": {
            "index": "name",
            "wildcard": {
              "query": "*" + query + "*",
              "path": ["name", "genre", "prompt"],
              "allowAnalyzedField": True
            }
        }
      },
      {"$limit": limit },
      {
        "$project": {
          "_id": 0,
          "name": 1,
          "genre": 1,
          "prompt": 1,
          "user_id": 1,
          "created_at": 1,
          "store_path": 1
        }
      }
  ])
  return results

def semantic_search_by_name(query, limit = 10):
  results = collection.aggregate([
    {
      "$vectorSearch": {
        "queryVector": asyncio.run(hf_embedding(query)),
        "path": "embedded_name",
        "numCandidates": 100,
        "limit": limit, # Control how many you result you want to get.
        "index": "name_vector_index",
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

def semantic_search_by_audio(file_path, limit = 10):
  results = collection.aggregate([
    {
      "$vectorSearch": {
        "queryVector": audio_embedding(file_path),
        "path": "embedded_audio",
        "numCandidates": 100,
        "limit": limit, # Control how many you result you want to get.
        "index": "embedded_audio_vector_index",
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
    }
  ])
  return results


if __name__ == "__main__":
  # example
  query = "nostalgic"
  file_path = "./sample/tmpte4m9jx6.wav"

  print("==============expamle: keyword_search_by_name================")
  results = keyword_search(query)

  for embedded_music in results:
    print(embedded_music)

  print("==============expamle: semantic_search_by_prompt=============")
  results = semantic_search_by_prompt(query)
  for embedded_music in results:
    print(embedded_music)

  print("==============expamle: semantic_search_by_audio==============")
  results = semantic_search_by_audio(file_path)
  for embedded_music in results:
    print(embedded_music)