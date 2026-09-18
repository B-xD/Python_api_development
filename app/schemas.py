from pydantic import BaseModel, EmailStr
from datetime import datetime



class PostBase(BaseModel):
    title: str 
    content: str
    published: bool = True 

class PostCreate(PostBase):
    pass

#enheritance helps us avoid duplicates 
class Post(PostBase): #we are defining what we want to get back to the user when they publish a post 
    id: int 
    created_at: datetime 

    class config:
        orm_mode = True #this takes away the dictionary error 


class UserCreate(BaseModel):
    email: EmailStr
    password: str 

class UserOut(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime

    class config:
            orm_mode = True


class UserLogin(BaseModel):
     email: EmailStr
     password: str 