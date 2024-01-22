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

@strawberry.mutation
def create_user(input: UserInput):
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
            'hashed_password': input.hashed_password,
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

def delete_user(username: str):
    db = Prisma()
    db.connect()
    user = db.user.delete(where={'username': username})
    db.disconnect()
    return user

