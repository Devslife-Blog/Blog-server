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
    fullname: str
    email: str
    password: str
    profile_image: str | None = None


class User(UserCreate):
    id: int
    blogs: List[Blog] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str


class SignupRequestBase(BaseModel):
    username: str
    fullname: str
    email: str
    detail: str
    request_at: date


class SignupRequestCreate(SignupRequestBase):
    password: str


class SignupRequest(SignupRequestCreate):
    id: int


class AnswerSignupRequest(BaseModel):
    request_id: int
    answer: bool = False
