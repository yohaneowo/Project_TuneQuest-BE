import strawberry
from datetime import datetime
from typing import Optional
@strawberry.type
class User:
    user_id = strawberry.ID
    username: str
    display_name: str
    gender: str
    created_at: str
    updated_at: str
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
    display_name: Optional[str] = None
    gender: Optional[str] = None
    created_at: Optional[str]
    updated_at: Optional[str]
    email: Optional[str] = None
    region: Optional[str] = None
    password: str
    profileimg_url: Optional[str] = None
    profilebanner_url: Optional[str] = None
    DOB: Optional[str] = None
    phone_number: Optional[str] = None
    about: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    address: Optional[str] = None
class UserInDB(User):
    hashed_password: str


