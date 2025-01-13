from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from jwt_token import SECRET_KEY, ALGORITHM, verify_token
import schemas

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login ") #here we are defining that from which route we are getting token in our case we are getting it from login route


def get_current_user(token :str=Depends(oauth2_scheme)):
    invalid_crediantials_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate the crediantials",
        headers={"WW-Authenticate":"Bearer"},
    )
    return verify_token(token, invalid_crediantials_exception)
    