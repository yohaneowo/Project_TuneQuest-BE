from prisma import Prisma
import strawberry
from src.model.User import UserInput , User
def get_user(username: str) -> User | None:
    db = Prisma()
    db.connect()
    try :
        user = db.user.find_unique(where={'username': username})
        return user
    except Exception as e:
        print(e)
        return None
    finally:
        db.disconnect()

def get_users() -> list[User] | None:
    db = Prisma()
    db.connect()
    users = db.user.find_many()
    db.disconnect()
    return users

def get_email(email: str) -> User | None:
    db = Prisma()
    db.connect()
    try :
        user = db.user.find_unique(where={'email': email})
        return user
    except Exception as e:
        print(e)
        return None
    finally:
        db.disconnect()
