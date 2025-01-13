from datetime import timedelta, datetime, timezone
from jose import JWTError, jwt
from fastapi import status, HTTPException
import schemas

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy() #copying the data passed to to_encode variable
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta #check to expiration time if provided otherwise it will add 30 minutes for current time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire}) #add time to to_encode dictionary
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # encode the data (to_encode according to secret key and algorithm)
    return encoded_jwt

def verify_token(token :str, invalid_crediantials_exception):
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email:str= payload.get("sub")
        if user_email is None:
            raise invalid_crediantials_exception
        token_data=schemas.TokenData(useremail=user_email) # returning the token data based in tokendata schema we have created in schemas.py file
    except JWTError:
        raise invalid_crediantials_exception