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
from alembic import command 

# the url schema SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>:<port_number>/<database_name>
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
#create an engine
engine = create_engine(SQLALCHEMY_DATABASE_URL) #the engine is responsable for the connection

#the session is used to talk to DB
TestingSessionLocal = sessionmaker(autocommit=False, autoflush= False, bind = engine)


@pytest.fixture(scope = 'function')
def session():
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine) 
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope = 'function')
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)