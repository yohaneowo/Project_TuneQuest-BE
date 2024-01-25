from prisma import Prisma
import strawberry
from src.model.User import UserInput
from src.middlewares.user import isUserExists , isEmailExists
from src.dao.user.error import *
from src.middlewares.register import hash_password

def create_user(input: UserInput) -> Response | None:
    if isUserExists(input.username):
        raise Exception("User Already Exists")
    if isEmailExists(input.email):
        raise Exception("Email Already Exists")
    db = Prisma()
    db.connect()
    hashed_password = hash_password(input.password)
    user = db.user.create(
        {
            'username': input.username,
            'display_name': input.display_name,
            'gender': input.gender,
            'created_at': input.created_at,
            'updated_at': input.updated_at,
            'email': input.email,
            'region': input.region,
            'hashed_password': hashed_password,
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
