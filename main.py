import os
from dotenv_vault import load_dotenv
import uvicorn
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from prisma import Prisma
from src.graphql.schema import graphql_app
from loguru import logger
from src.routes import auth
from src.routes.auth import oauth2_bearer
logger.add(
    sink=os.path.join('./logs', 'service.log'),
    rotation='500 MB',                  # 日志文件最大限制500mb
    retention='30 days',                # 最长保留30天
    format="{time}|{level}|{message}",  # 日志显示格式
    compression="zip",                  # 压缩形式保存
    encoding='utf-8',                   # 编码
    level='DEBUG',                      # 日志级别
    enqueue=True,                       # 默认是线程安全的，enqueue=True使得多进程安全
)

# logger.debug("详细调试信息")
# logger.info("普通信息")
# logger.success("成功信息")
# logger.warning("警告信息")
# logger.error("错误信息")
# logger.trace("异常信息")
# logger.critical("严重错误信息")

load_dotenv()
app = FastAPI()
logger.success("TuneQuest Service Started")

fastapi_port = os.getenv("FASTAPI_PORT")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(graphql_app, prefix="/graphql")
app.include_router(auth.router)


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
async def say_hello(token: Annotated[str, Depends(oauth2_bearer)]):
    print(fastapi_port)

    return {"message": f"Hello "}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(fastapi_port))