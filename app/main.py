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
from .routers import posts, user, auth


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

#rout the pap funciton to the user and post files so we may replace @app with @router
app.include_router(posts.router) 
app.include_router(user.router)
app.include_router(auth.router)

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

#extract the index of a post 
def find_index_posts(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i 
               

