""" 
Here we define models.
everymodel will be a table in the DB
"""
from sqlalchemy import Column, Integer, String, Boolean, text 
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base 




class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key= True, nullable = False)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    published = Column(Boolean, server_default = 'True', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)

#to create the model we use models.Base.metadata.create_all(bind=engine) -> add it to fastapi 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, nullable = False)
    email = Column(String, nullable = False, unique= True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
       