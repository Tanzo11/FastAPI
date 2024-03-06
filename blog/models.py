from typing import List
from pydantic import BaseModel, validator , EmailStr 

class Blog(BaseModel):
    title: str
    body: str


class BlogBase(Blog):
    class Config():
        from_attributes =True     
    


"""class ShowBlog(Blog):
    class Config():
        orm_mode=True"""




class User(BaseModel):
    name:str
    email: EmailStr
    password:str
    phone:str

    @validator("phone")

    def check_key_length(cls,value):
        if len(value)!=10 or not(value.isdigit()):
            raise ValueError("Enter valid phone number")
        return value


class ShowUser(BaseModel):
    name:str
    email:str
    phone:str 
    blogs : List[BlogBase]=[]
    class Config():
        from_attributes =True     
    
class ShowBlog(BaseModel):
    title:str
    body:str
    #creator: ShowUser
    class Config():
        #orm_mode=True
        from_attributes =True

class Login(BaseModel):
    #name: str
    email: EmailStr
    password:str
    """class Config():
        from_attributes =True"""
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None