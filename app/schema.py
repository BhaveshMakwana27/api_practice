from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id : int
    email : EmailStr

    class Config:
        orm_model=True

class Post(PostBase):
    id : int
    created_at : datetime
    owner : UserOut
    
    class Config:
        orm_mode=True

class PostOut(BaseModel):
    Post : Post
    votes : int

    class Config:
        orm_model=True

class UserBase(BaseModel):
    email : EmailStr
    password : str

class CreateUser(UserBase):
    pass


class UserLogin(BaseModel):
    email : EmailStr
    password : str


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None



class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)