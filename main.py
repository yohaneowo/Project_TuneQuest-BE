import os
from dotenv_vault import load_dotenv
import uvicorn

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from prisma import Prisma
from src.graphql.schema import graphql_app

load_dotenv()
app = FastAPI()
fastapi_port = os.getenv("FASTAPI_PORT")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(graphql_app, prefix="/graphql")
# @app.get("/")
# async def root(token: Annotated[str, Depends(oauth2_scheme)]):
#     # return {"message": "Hello World"}
#     return {"token": token}

@app.get("/")
def list_post():
    db = Prisma()

    db.connect()
    posts = db.user.find_many()
    db.disconnect()
    return posts

@app.get("/hello")
async def say_hello(name: str):
    print(fastapi_port)
    await generate_music_by_local()

    return {"message": f"Hello {result}"}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(fastapi_port))