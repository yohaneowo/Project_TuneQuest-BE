import strawberry
from src.controller.user import *
@strawberry.type
class Mutation:
    create_user: UserInput = strawberry.mutation()
