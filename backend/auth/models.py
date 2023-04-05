from pydantic import BaseModel
from typing import Optional
from fastapi.param_functions import Form
from datetime import datetime

from database.enum_list import Role

class Token(BaseModel):
    access_token: str
    token_type: str
    role: Optional[str]


class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None


class User(BaseModel):
    id: Optional[int]
    username: str
    password: Optional[str]
    role: str  # Admin User Guest
    verified: Optional[bool]
    createAt: Optional[datetime]
    email: Optional[str]

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

class ForgetPasswordInput():
    email: str

    def __init__(
        self,
        email: str = Form(),
    ):
        self.email=email


class PasswordChangingInput():
    code: str
    new_password: str

    def __init__(
        self,
        code: str = Form(),
        new_password: str = Form(),
    ):
        self.code=code
        self.new_password=new_password