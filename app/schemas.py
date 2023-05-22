from pydantic import BaseModel, EmailStr
from pydantic.types import conint
import email_validator
from datetime import datetime
from typing import Optional
# class Post(BaseModel): 

#     title: str
#     content: str
#     published: bool = True
#     # rating: Optional['int'] = None

class PostBase(BaseModel):
    # https://docs.pydantic.dev/usage/types/
    # the class to automatically check whether parameters 
    # are the same as the required
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class PropertyAddress(BaseModel):
    no_street: str 
    street_name: str 
    street_type: str 
    suburb: str 
    postcode: int

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post 
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    vote_dir: bool

class VoteOut(BaseModel):
    # user_id: int 
    post_id: int