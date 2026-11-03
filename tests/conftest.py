from fastapi.testclient import TestClient
from app.main import app 
from sqlalchemy import create_engine 
from sqlalchemy.orm import create_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import schemas, models 
from app.config import settings
from app.database import get_db, Base 
import pytest 
from alembic import command 
from app.oauth2 import create_access_token

# the url schema SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>:<port_number>/<database_name>
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:belton001@localhost/fastapi_test'

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

@pytest.fixture(scope ='function')
def test_user(client):
    user_data ={'email': 'johnrock@mail.com', 
                'password': 'john123'}
    
    res = client.post('/users', json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user 

@pytest.fixture(scope ='function')
def test_user_2(client):
    user_data ={'email': 'PaulRock@mail.com', 
                'password': 'Paul123'}
    
    res = client.post('/users', json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user 

@pytest.fixture 
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture 
def authorize_client(client, token):
    client.headers ={
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client 

@pytest.fixture
def test_posts(test_user, session, test_user_2):
    post_data = [
        {'title': 'The day of the Lord', 
         'content': 'The day of the Lord will me a terrible day for some and a glorious day for others', 
         'owner_id': test_user['id']},
        
        {'title': 'The Lord is my shepherd', 
         'content': 'He makes me lie down in green pastures and leads me beside quiet waters', 
         'owner_id': test_user['id']},

        {'title': 'Faith over fear', 
         'content': 'Even in the darkest valley, trust that the light is already on its way', 
         'owner_id': test_user['id']},

         {'title': 'We are gointo to party', 
           'content': 'Yolo Yolo Yolo', 
           'owner_id': test_user_2['id']}

    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, post_data)
    posts = list(post_map)
    session.add_all(posts)

    # session.add_all([
    #     models.Post(tittle= 'The day of the Lord', 
    #      content ='The day of the Lord will me a terrible day for some and a glorious day for others', 
    #      owner_id= test_user['id']),
    #      models.Post(tittle= 'The Lord is my shepherd', 
    #      content = 'He makes me lie down in green pastures and leads me beside quiet waters', 
    #      owner_id = test_user['id']    
    #      ),
    #      models.Post(tittle = 'Faith over fear', 
    #      content= 'Even in the darkest valley, trust that the light is already on its way', 
    #      owner_id = test_user['id']
             
    #      )   
    #     ])
    session.commit()
    posts = session.query(models.Post).all()

    return posts
