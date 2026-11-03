from fastapi import FastAPI, Response, status, HTTPException, Depends 
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional 
from random import randrange 
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import engine, get_db
from sqlalchemy.orm import Session 
from . import models 
import time

models.Base.metadata.create_all(bind=engine)
 
app = FastAPI()


#create a test endpoint for the SQL DB
@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all() #allows us to access the Post model/table and all the entries in it 
    return {'data': posts}


class Post(BaseModel):
    title: str 
    content: str
    published: bool = True 

while True:
#we use the try statement whenever there is something that can fail 
    try:
        conn = psycopg2.connect(host='localhost', database = 'fastapi', user='postgres',
                                password='belton001', cursor_factory=RealDictCursor) #RealDictCursor will give you the column name and a value 

        cursor = conn.cursor()
        print("--DATA BASE CONNECTION WAS SUCCESSFUL")
        break 
    except Exception as e:
        print("--connection to database failed")
        print(f"Error: {e}")
        time.sleep(2)


my_post =[
    {"title": "title for post 1",
     "content": "content for post 1",
     "id": 1},
     {"title": "favorite food",
      "content": "I love pizza",
      "id": 2
      }
]

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

#extract the index of a post 
def find_index_posts(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i 
               
@app.get("/")
def root():

    return {'message': 'Welcome to my API'}

#retrieve posts from the DB and posting it 
@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

#create a new post 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post): 
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published)) #%s are placeholders for the actual values we want to enter
# this avoids SQL injections 

    new_post = cursor.fetchone()
    #commit the changes (to save to db)
    conn.commit()

    return {"data" : new_post}

@app.post("/createposts")
def create_post(new_post:Post): #this extracts all of the fields from body, converts them into a python dictionary and stores it inside a variable called payload/new_data 
    print(new_post)
    print(new_post.dict()) #new_post.dict() will convert the output in to a dict
    return {"data" : new_post}

#fetching a post by ID 
@app.get("/posts/{id}") 
def get_posts(id: int, response: Response):

    cursor.execute("""SELECT * FROM posts WHERE id = %s""",
                   (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND,
                            detail =f"post with id: {id} was not found")
        
    return {"post_detail": post}

    
#deleting a post 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int ):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
                   (str(id)))

    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")

    #commit changes 
    conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#updading a post 
@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id:{id} does not exist")
    
    return {"data": updated_post}
    +================================
    @app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post, db: Session = Depends(get_db)): 
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
                   #(post.title, post.content, post.published)) #%s are placeholders for the actual values we want to enter
# this avoids SQL injections 

    #new_post = cursor.fetchone()
    #commit the changes (to save to db)
    #conn.commit()
    
    new_post =models.Post(
        title=post.title, content = post.content, published = post.published)
    db.add(new_post) #this adds the newly created post to the DB
    db.commit() #commit the new added post to DB
    db.refresh(new_post) #return the new post like RETURNING
    return {"data" : new_post}

============================= Sept 17===
from fastapi import FastAPI, Response, status, HTTPException, Depends 
from fastapi.params import Body
from random import randrange 
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import engine, get_db
from sqlalchemy.orm import Session 
from . import models, schemas #imports the entire file 
import time

models.Base.metadata.create_all(bind=engine)
 
app = FastAPI()

while True:
#we use the try statement whenever there is something that can fail 
    try:
        conn = psycopg2.connect(host='localhost', database = 'fastapi', user='postgres',
                                password='belton001', cursor_factory=RealDictCursor) #RealDictCursor will give you the column name and a value 

        cursor = conn.cursor()
        print("--DATA BASE CONNECTION WAS SUCCESSFUL")
        break 
    except Exception as e:
        print("--connection to database failed")
        print(f"Error: {e}")
        time.sleep(2)


my_post =[
    {"title": "title for post 1",
     "content": "content for post 1",
     "id": 1},
     {"title": "favorite food",
      "content": "I love pizza",
      "id": 2
      }
]

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

#extract the index of a post 
def find_index_posts(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i 
               
@app.get("/")
def root():

    return {'message': 'Welcome to my API'}


#retrieve posts from the DB and posting it 
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

#create a new post 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:schemas.Post, db: Session = Depends(get_db)): 
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
                   #(post.title, post.content, post.published)) #%s are placeholders for the actual values we want to enter
# this avoids SQL injections 

    #new_post = cursor.fetchone()
    #commit the changes (to save to db)
    #conn.commit()

    new_post =models.Post(**post.dict()) #this will unpack the dictionary into the previous Post.title model, and we dont need to manually add each field 
    db.add(new_post)
    db.commit() #commit the new added post to DB
    db.refresh(new_post) #return the new post like RETURNING
    return {"data" : new_post}

@app.post("/createposts")
def create_post(new_post:schemas.PostCreate): #this extracts all of the fields from body, converts them into a python dictionary and stores it inside a variable called payload/new_data 
    print(new_post)
    print(new_post.dict()) #new_post.dict() will convert the output in to a dict
    return {"data" : new_post}

#fetching a post by ID 
@app.get("/posts/{id}") 
def get_posts(id: int, db: Session = Depends(get_db)):

    #cursor.execute("""SELECT * FROM posts WHERE id = %s""",
     #              (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first() #dotfirst replaces dotall becasue once we find the post with that unique Id we can then stop
    if not post:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND,
                            detail =f"post with id: {id} was not found")
        
    return {"post_detail": post}

    
#deleting a post 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db) ):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
     #              (str(id)))

    #deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")

    deleted_post.delete(synchronize_session = False) # this is the default configutation
    db.commit()
    #commit changes 
    #conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#updading a post 
@app.put("/posts/{id}")
def update_post(id:int, post:schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #               (post.title, post.content, post.published, str(id)))

    #updated_post = cursor.fetchone()
    #conn.commit()
    query_post = db.query(models.Post).filter(models.Post.id == id)
    post_ = query_post.first()
    if post_ == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id:{id} does not exist")

    query_post.update(post.dict(), synchronize_session = False)
    db.commit()

    return {"data": query_post.first()}
    
    ======================== Sept 18===
    from fastapi import FastAPI, Response, status, HTTPException, Depends 
from fastapi.params import Body
from typing import Optional, List
from random import randrange 
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import engine, get_db
from sqlalchemy.orm import Session 
from . import models, schemas, utils #imports the entire file 
import time


models.Base.metadata.create_all(bind=engine)
 
app = FastAPI()

while True:
#we use the try statement whenever there is something that can fail 
    try:
        conn = psycopg2.connect(host='localhost', database = 'fastapi', user='postgres',
                                password='belton001', cursor_factory=RealDictCursor) #RealDictCursor will give you the column name and a value 

        cursor = conn.cursor()
        print("--DATA BASE CONNECTION WAS SUCCESSFUL")
        break 
    except Exception as e:
        print("--connection to database failed")
        print(f"Error: {e}")
        time.sleep(2)


my_post =[
    {"title": "title for post 1",
     "content": "content for post 1",
     "id": 1},
     {"title": "favorite food",
      "content": "I love pizza",
      "id": 2
      }
]

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

#extract the index of a post 
def find_index_posts(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i 
               
@app.get("/")
def root():

    return {'message': 'Welcome to my API'}


#retrieve posts from the DB and posting it 
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return  posts

#create a new post 
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db)): 
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
                   #(post.title, post.content, post.published)) #%s are placeholders for the actual values we want to enter
# this avoids SQL injections 

    #new_post = cursor.fetchone()
    #commit the changes (to save to db)
    #conn.commit()

    new_post =models.Post(**post.dict()) #this will unpack the dictionary into the previous Post.title model, and we dont need to manually add each field 
    db.add(new_post)
    db.commit() #commit the new added post to DB
    db.refresh(new_post) #return the new post like RETURNING
    return new_post

@app.post("/createposts")
def create_post(new_post:schemas.PostCreate): #this extracts all of the fields from body, converts them into a python dictionary and stores it inside a variable called payload/new_data 
    print(new_post)
    print(new_post.dict()) #new_post.dict() will convert the output in to a dict
    return {"data" : new_post}

#fetching a post by ID 
@app.get("/posts/{id}", response_model=schemas.Post) 
def get_posts(id: int, db: Session = Depends(get_db)):

    #cursor.execute("""SELECT * FROM posts WHERE id = %s""",
     #              (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first() #dotfirst replaces dotall becasue once we find the post with that unique Id we can then stop
    if not post:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND,
                            detail =f"post with id: {id} was not found")
        
    return post

    
#deleting a post 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db) ):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
     #              (str(id)))

    #deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")

    deleted_post.delete(synchronize_session = False) # this is the default configutation
    db.commit()
    #commit changes 
    #conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#updading a post 
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #               (post.title, post.content, post.published, str(id)))

    #updated_post = cursor.fetchone()
    #conn.commit()
    query_post = db.query(models.Post).filter(models.Post.id == id)
    post_ = query_post.first()
    if post_ == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id:{id} does not exist")

    query_post.update(post.dict(), synchronize_session = False)
    db.commit()

    return query_post.first()


#create a path for users to send data to the DB
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session =Depends(get_db)):

    #hash the password - user.password 
    hashed_password = utils.hash(user.password)
    user.password = hashed_password #this will replace the pydentic user password with the hash

    new_user = models.User(**user.dict())  
    db.add(new_user)
    db.commit() 
    db.refresh(new_user) #return the new post like RETURNING

    return new_user

@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'User with id: {id} does not exist')

    return user 

====================== Sep 19
app/routers/auth.py 

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from .. import database, schemas, models, utils, auth2  

router = APIRouter(
    tags = ['Authentication']
    )

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = 'Invalid Credentials')

    if not utils.verify(user_credentials.password, user.password):

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = 'Invalid Credentials')

    #create token 
    access_token = auth2.create_access_token(data = {"user_id" : user.id}) #put all information you want to pass

    #return token 
    return {"access_token": access_token, "token_type": "bearer"} #you configure the token type in the frontend 

#then go to the jwt website pass the token generated to see whats in the token

=================
auth.py 

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from .. import database, schemas, models, utils, auth2  

router = APIRouter(
    tags = ['Authentication']
    )

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = 'Invalid Credentials')

    if not utils.verify(user_credentials.password, user.password):

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = 'Invalid Credentials')

    #create token 
    access_token = auth2.create_access_token(data = {"user_id" : user.id}) #put all information you want to pass

    #return token 
    return {"access_token": access_token, "token_type": "bearer"} #you configure the token type in the frontend 

#then go to the jwt website pass the token generated to see whats in the toke

================== sept 21 

from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


#this will be our login endpoint 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login')

#SECRET_KEY
#Algorithm 
#expiration time for our token -- so users dont have to login forever

#run openssl rand -hex 32 to get a string like the one below
SECRET_KEY = 'e78a9ac5d0ed615a0e736dbc2157078ff9ba7785d871327fb6be84746d271e8f'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # 60 min 

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
        token_data = schemas.TokenData(id = "id") # this will insure that all the data that we pass is actually there 
    except JWTError: 
        raise credetials_exception

    return token_data

#verify if the token is valid add the paramenter 
def get_current_user(token: str= Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    #define the credential exception: when the credentials are wrong 
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail = "could not find valid credentials",
                                           headers={"WWW-Authenticate": "Bearer"}  )

    #token = verify_access_token(token, credential_exception)
    #user = db.query(models.User).filter(models.User.id == token.id).first()

    return verify_access_token(token, credential_exception)
=========== if you want to retrieve the logged in user posts only ===========
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int =
                Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return  posts

@router.get("/{id}", response_model=schemas.Post) 
def get_posts(id: int, db: Session = Depends(get_db), current_user: int =
                Depends(oauth2.get_current_user)):

    #cursor.execute("""SELECT * FROM posts WHERE id = %s""",
     #              (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first() #dotfirst replaces dotall becasue once we find the post with that unique Id we can then stop
    if not post:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND,
                            detail =f"post with id: {id} was not found")
    if post.owner_id  != current_user.id:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                                detail = "unauthorized to perform requested action")
  
    return post

    # {{URL}}posts?search=Post%20two %20 means space 

    =======
    from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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

================testing the apis ===========
from fastapi.testclient import TestClient
from app.main import app 
from sqlalchemy import create_engine 
from sqlalchemy.orm import create_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import schemas 
from app.config import settings
from app.database import get_db, Base 
import pytest 

# the url schema SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>:<port_number>/<database_name>
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:belton001@localhost/fastapi_test'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
#create an engine
engine = create_engine(SQLALCHEMY_DATABASE_URL) #the engine is responsable for the connection

#the session is used to talk to DB
TestingSessionLocal = sessionmaker(autocommit=False, autoflush= False, bind = engine)

#create a dependecy function to start and close sessions 
def overide_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = overide_get_db

@pytest.fixture
# def client():
#     #run the code before running the test (create a table)
#     Base.metadata.create_all(bind=engine) 
#     yield TestClient(app)
#     #run the code after running the test (drop the table)
#     Base.metadata.drop_all(bind=engine) 
def client():
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine) 
    yield TestClient(app)
    
def test_root(client):
    res = client.get('/')
    print(res.json().get('message'))
    assert res.json().get('message') == 'Shallom Adonai !!!'
    assert res.status_code == 200


def test_create_user(client):
    res =client.post('/users', json={'email': 'johnrock@mail.com', 'password': 'john123'})
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'johnrock@mail.com'
    assert res.status_code == 201

#pytest tests/test_users.py -v


---- build tables with alembic 
def client():
    # Base.metadata.drop_all(bind=engine) 
    # Base.metadata.create_all(bind=engine) 
    command.upgrade('head')
    yield TestClient(app)
    commmand.downgrade('base')

==== my test that worked 
def test_create_post(authorize_client, test_posts, title, content, published):
    res = authorize_client.post('/posts/', json={'title': 'The day of the Lord', 'content': 'The day of the Lord will me a terrible day for some and a glorious day for others', 'published': 'True'})

    #res = client.post('/posts/', json={'tittle': 'The day of the Lord', 'content': 'The day of the Lord will me a terrible day for some and a glorious day for others', 'published': 'True'})

    #new_post = schemas.PostOut(**res.json()) 
    print(res.json())
    assert res.status_code == 201 