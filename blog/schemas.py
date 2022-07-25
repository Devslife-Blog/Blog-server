from typing import List
from datetime import date

from pydantic import BaseModel


class BlogBase(BaseModel):

    title: str
    description: str
    date: date


class BlogShow(BlogBase):
    content: str


class Blog(BlogShow):
    id: int


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    fullanme: str
    email: str
    password: str
    profile_image: str | None = None


class User(UserCreate):
    id: int
    blogs: List[Blog] = []
