
def isUserExists(username: str):
    from src.dao.user.query import get_user
    user = get_user(username)
    if not user:
        return False
    return True