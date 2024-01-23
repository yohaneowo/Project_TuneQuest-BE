import strawberry
from src.dao.user.mutation import *
from src.model.User import User



@strawberry.type
class Mutation:
    create_user: User = strawberry.mutation(resolver=create_user)