from typing import Optional

from pydantic import BaseModel, Field


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class User(BaseModel):
    username: str = Field(..., description="user username")
    email: str = Field(..., description="user email")
    password: str = Field(..., description="user password")


class Post(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)

class UpdatePost(BaseModel):
    title: Optional[str] = Field(default=None, description="updated title")
    content: Optional[str] = Field(default=None, description="updated content")
