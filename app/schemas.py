
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

# Define class, extend BaseModel - pydantic - This is for schema and validation
class PostBase(BaseModel):
    title:  str
    content: str
    published: bool = False    

class PostCreate(PostBase):        
    pass


# Response schema for user output and by id
class UserOutput(BaseModel):
    id: int
    email: EmailStr
    created_At: datetime

    class Config:
        orm_mode = True

# This is for response
class Post(PostBase):
    id: int
    created_At: datetime
    owner_id: int
    owner: UserOutput

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    Votes: int

    class Config:
        orm_mode = True

# Request schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str



# schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# schema for access token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
            
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)