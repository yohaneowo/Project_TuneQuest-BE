from passlib.context import CryptContext
from src.controller.user import get_user
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

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


SECRET_KEY = 'e1464563b1abb0b5741028bd682872bd9d4a4717bb7118e6d9c9d29296d64e29'
# 加密算法
ALGORITHM = "HS256"
# 过期时间，分钟
ACCESS_TOKEN_EXPIRE_MINUTES = 30