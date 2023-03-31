from pydantic import BaseModel
from typing import Optional
from fastapi.param_functions import Form

from database.enum_list import Role

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: Optional[int]
    username: str
    password: Optional[str]
    role: str  # Admin User Guest
    verified: Optional[bool]

    class Config:
        orm_mode = True


class RegisterInput():
    username: str
    password: str
    email: str
    role: Role

    def __init__(
        self,
        username: str = Form(),
        password: str = Form(),
        email: str = Form(),
        role: Role = Form()
    ):
        self.username=username
        self.password=password
        self.email=email
        self.role=role

