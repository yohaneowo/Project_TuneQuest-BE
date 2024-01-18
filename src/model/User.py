from pydantic import BaseModel, Field
from typing import Union, Optional
from datetime import datetime
class User(BaseModel):
    user_id: int = Field(..., alias="user_id")
    username: str = Field(..., alias="username")
    display_name: Optional[str] = Field(None, alias="display_name")
    gender: Optional[str] = Field(None, alias="gender")
    profilebanner_url: Optional[str] = Field(None, alias="profilebanner_url")
    created_at: datetime = Field(..., alias="created_at")
    updated_at: datetime = Field(..., alias="updated_at")
    email: Optional[str] = Field(None, alias="email")
    region: Optional[str] = Field(None, alias="region")
    hashed_password: str = Field(..., alias="hashed_password")
    profileimg_url: Optional[str] = Field(None, alias="profileimg_url")
    DOB: Optional[datetime] = Field(None, alias="DOB")
    phone_number: Optional[int] = Field(None, alias="phone_number")
    about: Optional[str] = Field(None, alias="about")
    first_name: Optional[str] = Field(None, alias="first_name")
    last_name: Optional[str] = Field(None, alias="last_name")
    full_name: Optional[str] = Field(None, alias="full_name")
    address: Optional[str] = Field(None, alias="address")
class UserInDB(User):
    hashed_password: str


