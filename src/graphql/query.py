import strawberry
from src.model.User import User
from src.dao.user.query import *
@strawberry.type
class Query:
    user: User | None = strawberry.field(resolver=get_user)
    users: list[User] = strawberry.field(resolver=get_users)


