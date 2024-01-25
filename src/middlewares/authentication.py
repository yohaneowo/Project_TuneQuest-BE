from passlib.context import CryptContext
from src.dao.user.query import get_user
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os
load_dotenv()
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
# 加密算法
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    # 1、通过用户名模拟去数据库查找用户
    user = get_user(username)
    if not user:
        # 2、用户不存在
        return False
    if not verify_password(password, user.hashed_password):
        # 3、密码验证失败
        return False
    # 4、验证通过，返回用户信息
    return user

def create_access_token(data: dict, expires_delta: timedelta):
    # 1、设置过期时间
    expire = datetime.utcnow() + expires_delta
    # 2、设置加密算法
    to_encode = data.copy()
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
