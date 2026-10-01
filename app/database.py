from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings 

# the url schema SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>:<port_number>/<database_name>
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:belton001@localhost/fastapi'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
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


# while True:
# #we use the try statement whenever there is something that can fail 
#     try:
#         conn = psycopg2.connect(host='localhost', database = 'fastapi', user='postgres',
#                                 password='belton001', cursor_factory=RealDictCursor) #RealDictCursor will give you the column name and a value 

#         cursor = conn.cursor()
#         print("--DATA BASE CONNECTION WAS SUCCESSFUL")
#         break 
#     except Exception as e:
#         print("--connection to database failed")
#         print(f"Error: {e}")
#         time.sleep(2)