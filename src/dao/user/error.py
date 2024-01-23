import strawberry
from src.model.User import User
from typing import Annotated, Union


@strawberry.type
class RegisterUserSuccess:
    user: User


@strawberry.type
class UsernameAlreadyExistsError:
    username: str


# Create a Union type to represent the 2 results from the mutation
Response = Annotated[
    Union[RegisterUserSuccess, UsernameAlreadyExistsError],
    strawberry.union("RegisterUserResponse"),
]
