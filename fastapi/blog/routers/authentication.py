import sys
from pathlib import Path
# Add the parent folder to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from fastapi import APIRouter, Depends, status, HTTPException
import schemas
import database
import models
from sqlalchemy.orm import Session
from hashing import Hash
import jwt_token
from fastapi.security import OAuth2PasswordRequestForm

router= APIRouter(
    tags=['Login']
)



@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(), db:Session= Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.name==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid username {request.username}')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid password')
    #generate a jwt token and return that
    #access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_token.create_access_token(
        data={"sub": user.email})#we are passing useremail with 'sub' as key in data dictionary
    return {'access_token':access_token, 'token_type':"bearer"}
    #return user