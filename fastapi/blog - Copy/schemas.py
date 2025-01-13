from pydantic import BaseModel


class Blog(BaseModel):
    title:str
    body:str


class Showblog(BaseModel):# this is response model class which is used todefine the response as we required here we are only getting the title as respose we can modily it according to our requirements
    title: str #column name
    body: str
    class Config():
        orm_mode=True

class user(BaseModel):
    name:str
    email: str
    password:str

class Showuser(BaseModel):
    name:str
    email:str
    class Config():
        orm_mode=True