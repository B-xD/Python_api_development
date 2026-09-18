from passlib.context import CryptContext

#define settings 
pwd_context = CryptContext(schemes =['bcrypt'], deprecated = 'auto')

#define a function for hash 
def hash(password: str):
    return pwd_context.hash(password)

#a function to compared the user's passwpord to the one in our DB
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) #verify is used to hash the password just as the hash function 
