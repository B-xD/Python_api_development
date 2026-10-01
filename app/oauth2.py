from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


#this will be our login endpoint 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

#SECRET_KEY
#Algorithm 
#expiration time for our token -- so users dont have to login forever

#run openssl rand -hex 32 to get a string like the one below
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes 

def create_access_token(data: dict):
    to_encode = data.copy()

    #create the expiration field
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return encode_jwt


def verify_access_token(token: str, credetials_exception):

    try:
        #decode the jwt 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        #extruct the ID 
        id:str = payload.get("user_id")

        if id is None:
            raise credetials_exception
        token_data = schemas.TokenData(id = id) # this will insure that all the data that we pass is actually there 
    except JWTError: 
        raise credetials_exception

    return token_data

#verify if the token is valid add the paramenter 
def get_current_user(token: str= Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    #define the credential exception: when the credentials are wrong 
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail = "could not find valid credentials",
                                           headers={"WWW-Authenticate": "Bearer"}  )

    token = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user