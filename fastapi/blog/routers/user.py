import sys
from pathlib import Path

# Add the parent folder to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import APIRouter, HTTPException, Depends,status,Response
import schemas
import models
import database
from sqlalchemy.orm import Session
from hashing import Hash

router= APIRouter(
    tags=['Users']
)


@router.post('/create_user')
def create_user(request:schemas.user, db:Session=Depends(database.get_db)):# this will create a new user and insert into the database users table
    #hashed_password=pwd_cxt.hash(request.password)#encryptting the password
    new_user=models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/show_users')#getting all the users from the database
def get_all_users(db:Session=Depends(database.get_db)):
    all_users=db.query(models.User).all()
    return all_users


@router.get('/user/{id}',response_model=schemas.Showuser)# get the user with id using reponse model
def get_user(id:int, db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not available')
    return user