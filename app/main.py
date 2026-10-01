from fastapi import FastAPI
from .database import engine
from . import models  #imports the entire file 
from .routers import posts, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine) #with alempic, we do not need this command 
 
app = FastAPI()

origins = ["*"] #every origin ["*"]

#cors
app.add_middleware(
    CORSMiddleware, #middleware is a function that runs before the request 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  #http methods to allow (get, put etc )
    allow_headers=["*"], # type of headers to allow 
)

#rout the pap funciton to the user and post files so we may replace @app with @router
app.include_router(posts.router) 
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def main():
    
    return {"message": "Shallom"}

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

#extract the index of a post 
def find_index_posts(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i 
               

