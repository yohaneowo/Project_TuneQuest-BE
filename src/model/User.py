import strawberry
from datetime import datetime
@strawberry.type
class User:
    user_id = strawberry.ID
    username: str
    display_name: str
    gender: str
    created_at: datetime
    updated_at: datetime
    email: str
    region: str
    hashed_password: str
    profileimg_url: str
    profilebanner_url: str
    DOB: datetime
    phone_number: int
    about: str
    first_name: str
    last_name: str
    full_name: str
    address: str

@strawberry.input
class UserInput:
    user_id = strawberry.ID
    username: str
    display_name: str
    gender: str
    created_at: datetime
    updated_at: datetime
    email: str
    region: str
    hashed_password: str
    profileimg_url: str
    profilebanner_url: str
    DOB: datetime
    phone_number: int
    about: str
    first_name: str
    last_name: str
    full_name: str
    address: str
class UserInDB(User):
    hashed_password: str


