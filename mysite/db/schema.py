from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import date
from .model import UserStatusChoice


class UserProfileRegisterSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    status: UserStatusChoice = UserStatusChoice.basic


class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr


class UpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    status: UserStatusChoice
    registered_date: date

    model_config = ConfigDict(from_attributes=True)


class UserLoginSchema(BaseModel):
    username: str
    password: str


class RequestUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    status: UserStatusChoice


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str



