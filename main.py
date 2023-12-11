import os
from fastapi import FastAPI
from dotenv_vault import load_dotenv
import uvicorn

load_dotenv()
app = FastAPI()
port = os.getenv("PORT")
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    print(port)
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(port))