    import os
from fastapi import FastAPI
from dotenv_vault import load_dotenv
import uvicorn

from typing import Annotated

from fastapi import Depends, FastAPI

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

load_dotenv()
app = FastAPI()
fastapi_port = os.getenv("FASTAPI_PORT")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.get("/")
async def root(token: Annotated[str, Depends(oauth2_scheme)]):
    # return {"message": "Hello World"}
    return {"token": token}


@app.get("/hello")
async def say_hello(name: str):
    print(fastapi_port)
    await generate_music_by_local()

    return {"message": f"Hello {result}"}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(fastapi_port))