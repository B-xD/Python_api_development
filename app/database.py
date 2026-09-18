from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# the url schema SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:belton001@localhost/fastapi'
#create an engine
engine = create_engine(SQLALCHEMY_DATABASE_URL) #the engine is responsable for the connection

#the session is used to talk to DB
SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind = engine)

#define baseclass 
Base = declarative_base()

#create a dependecy function to start and close sessions 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()