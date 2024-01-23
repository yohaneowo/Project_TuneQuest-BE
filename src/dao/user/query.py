from prisma import Prisma
import strawberry
from src.model.User import UserInput , User
def get_user(username: str) -> User | None:
    db = Prisma()
    db.connect()
    user = db.user.find_unique(where={'username': username})
    db.disconnect()
    return user

def get_users() -> list[User] | None:
    db = Prisma()
    db.connect()
    users = db.user.find_many()
    db.disconnect()
    return users
