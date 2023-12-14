import os
from fastapi import FastAPI
from dotenv_vault import load_dotenv
import uvicorn
from generate_music import *


load_dotenv()
app = FastAPI()
fastapi_port = os.getenv("FASTAPI_PORT")
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello")
async def say_hello(name: str):
    print(fastapi_port)
    await generate_music_by_local()

    return {"message": f"Hello {result}"}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(fastapi_port))