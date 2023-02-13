from pydantic import BaseModel
from typing import Optional

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

    class Config:
        orm_mode = True

