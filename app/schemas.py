from datetime import datetime
import email
from os import access
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(BasePost):
    pass

class UpdatePost(BasePost):
    pass

class UserCreatedResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class PostResponse(BasePost):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserCreatedResponse

    class Config:
        orm_mode = True

class PostVotesView(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str  

class UserCreated(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserFoundResponse(BaseModel):
    id: int
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)