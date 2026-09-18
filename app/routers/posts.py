from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session 
from .. import models, schemas #imports the entire file 

router = APIRouter(
    prefix="/posts" ,#this is to replace every /posts in out endpoints (@router.get("/posts")
    tags = ['posts'] # this will group all posts endpois together in docs. This improves the readability of our docs  
)

#retrieve posts from the DB and posting it 
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return  posts

#create a new post 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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


#fetching a post by ID 
@router.get("/{id}", response_model=schemas.Post) 
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
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
@router.put("/posts/{id}", response_model=schemas.Post)
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