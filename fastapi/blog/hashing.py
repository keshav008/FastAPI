from passlib.context import CryptContext


pwd_cxt=CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password:str):# function to encrypt the user password
        return pwd_cxt.hash(password)
    
    def verify(hashed_password, plain_password): #function to verify the plain password and hashed password
        return pwd_cxt.verify(plain_password,hashed_password)