from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Annotated
from jose import JWTError, jwt


SECRET_KEY = 'e1464563b1abb0b5741028bd682872bd9d4a4717bb7118e6d9c9d29296d64e29'
# 加密算法
ALGORITHM = "HS256"
# 过期时间，分钟
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")