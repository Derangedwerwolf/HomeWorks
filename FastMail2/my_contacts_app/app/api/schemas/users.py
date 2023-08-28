from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserDb(UserBase):
    id: int
    created_at: datetime
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


class TokenModel(UserBase):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(UserBase):
    user: UserDb
    tokens: TokenModel  # Include tokens here
    detail: str = "User successfully created"


class RequestEmail(BaseModel):
    email: EmailStr
