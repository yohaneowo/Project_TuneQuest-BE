from pydantic import BaseModel
from typing import Union
class User(BaseModel):
    username: str
    password: int
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str


