from app import schemas
import pytest 
from jose import JWTError, jwt 
from app.config import settings 


# def test_root(client):
#     res = client.get('/')
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Shallom Adonai !!!'
#     assert res.status_code == 200


def test_create_user(client):
    res =client.post('/users', json={'email': 'johnrock@mail.com', 'password': 'john123'})
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'johnrock@mail.com'
    assert res.status_code == 201

def test_login_user(test_user, client):
    res =client.post('/login', data={'username': test_user['email'], 'password': test_user['password']})
    
    # new_user = schemas.UserOut(**res.json())
    # assert new_user.email == 'johnrock@mail.com'
    print(res.json())
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms =[settings.algorithm])
    
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wring_email@mail.com', 'john123', 403 ),
    ('johnrock@mail.com', 'wrongp', 403),
    ('wrongemail@gmail.com', 'wrongpassword11', 403),
    ( None, 'john123', 422),
    ('johnrock@mail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code) :
    res = client.post('/login', data={'username': email, 'password': password})

    assert res.status_code == status_code 
    if status_code == 403:
        assert res.json().get('detail') == "Invalid Credentials"
#pytest tests/test_users.py -v
