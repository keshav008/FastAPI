from database import Base
from sqlalchemy import Column, Integer, String

class Blog(Base):# creating a class that maps to the table in the database
    __tablename__='blogs'# table name
    id=Column(Integer, primary_key=True, index=True) #these are the column names with type and attribues
    title=Column(String(100))
    body=Column(String(500))


class User(Base):# creating a class for users table
    __tablename__='users'
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String(100))
    email=Column(String(200))
    password=Column(String(100))
