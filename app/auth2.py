from jose import JWTError, jwt
from datetime import datetime, timedelta


#SECRET_KEY
#Algorithm 
#expiration time for our token -- so users dont have to login forever

#run openssl rand -hex 32 to get a string like the one below
SECRET_KEY = 'e78a9ac5d0ed615a0e736dbc2157078ff9ba7785d871327fb6be84746d271e8f'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

def create_access_token(data: dict):
    to_encode = data.copy()

    #create the expiration field
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return encode_jwt

