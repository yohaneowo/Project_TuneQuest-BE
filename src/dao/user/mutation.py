from prisma import Prisma
import strawberry
from src.model.User import UserInput
from src.middlewares.user import isUserExists
from src.dao.user.error import *


def create_user(input: UserInput) -> Response | None:
    if isUserExists(input.username):
        raise Exception("User Already Exists")

    db = Prisma()
    db.connect()
    user = db.user.create(
        {
            'username': input.username,
            'display_name': input.display_name,
            'gender': input.gender,
            'created_at': input.created_at,
            'updated_at': input.updated_at,
            'email': input.email,
            'region': input.region,
            'hashed_password': input.password,
            'profileimg_url': input.profileimg_url,
            'profilebanner_url': input.profilebanner_url,
            'DOB': input.DOB,
            'phone_number': input.phone_number,
            'about': input.about,
            'first_name': input.first_name,
            'last_name': input.last_name,
            'full_name': input.full_name,
            'address': input.address
        }
    )
    db.disconnect()
    return user
    # return response(message="User Created", status="200")


@strawberry.mutation
def delete_user(username: str) -> UserInput:
    db = Prisma()
    db.connect()
    user = db.user.delete(where={'username': username})
    db.disconnect()
    return user
