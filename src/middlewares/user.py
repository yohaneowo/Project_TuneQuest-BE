from prisma import Prisma

def isUserExists(username: str):
    from src.dao.user.query import get_user
    user = get_user(username)
    if not user:
        return False
    return True

def isEmailExists(email: str):
    from src.dao.user.query import get_email
    user = get_email(email)
    if not user:
        return False
    return True
