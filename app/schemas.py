from xmlrpc.client import DateTime
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #default of True makes it an optional field for the user input
    

class PostCreate(PostBase):
    pass                        #inherits from PostBase

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

#class to define response
class Post(PostBase):
    id: int
    #id = int
    created_at: datetime
    owner_id: int
    owner: UserOut

    #as explained in link, below is needed: https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
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
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
