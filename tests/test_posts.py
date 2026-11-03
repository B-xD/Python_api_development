from app.routers import posts 
from app import schemas 
import pytest

@pytest.mark.parametrize("title, content, published",[
    ('The day of the Lord', 'The day of the Lord will me a terrible day for some and a glorious day for others', True),
    ('The Lord is my shepherd', 'He makes me lie down in green pastures and leads me beside quiet waters', True),
    ('Faith over fear', 'Even in the darkest valley, trust that the light is already on its way', True)
    ])
def test_create_post(authorize_client, test_user, title, content, published):
    res = authorize_client.post('/posts/', json={'title': title, 'content': content, 'published': published})

    #res = client.post('/posts/', json={'tittle': 'The day of the Lord', 'content': 'The day of the Lord will me a terrible day for some and a glorious day for others', 'published': 'True'})

    new_post = schemas.Post(**res.json()) 
    print(new_post)
    assert res.status_code == 201 
    assert new_post.title == title 
    assert new_post.content == content 
    assert new_post.published == published
    assert new_post.owner_id == test_user['id'] 

def test_create_post_default_publish_True(authorize_client, test_user, test_posts):
    res = authorize_client.post(
        "/posts/", json={'title': 'arbitrary title', 'content': 'any content'}

    )
    new_post = schemas.Post(**res.json()) 
    assert res.status_code == 201 
    assert new_post.title == 'arbitrary title'
    assert new_post.content == 'any content'
    assert new_post.published == True
    assert new_post.owner_id == test_user['id']

    return 

def test_get_post(authorize_client, test_posts):
    res = authorize_client.get('/posts/')
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert  len(res.json()) == len(test_posts)
    assert res.status_code == 200
   # assert posts_list[0].post.id == test_posts[0].id

def test_unauthorized_user_get_posts(client, test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401

def test_unauthorized_user_get_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_get_post_nonexisting_id(authorize_client):
    res = authorize_client.get(f'/posts/888888888')

    assert res.status_code == 404 

def test_get_one_post(authorize_client, test_posts):
    res = authorize_client.get(f'/posts/{test_posts[0].id}')

    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_posts[0].id 
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

def test_unauthorized_user_get_post(client):
    res = client.post(
            "/posts/", json={'title': 'arbitrary title', 'content': 'any content'}
    
        )

    assert res.status_code == 401 

def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(
        f'/posts/{test_posts[0].id}'
    )
    assert res.status_code == 401

def test_delete_post_sucess(client, authorize_client, test_posts):

    res =authorize_client.delete(
        f'/posts/{test_posts[0].id}'
    )

    assert res.status_code == 204

def test_delete_post_not_exist(authorize_client):
    res = authorize_client.delete(
        f'/posts/{10000}'
    )

    assert res.status_code == 404 

def test_delete_other_user_post(authorize_client, test_posts):
    res = authorize_client.delete(
        f'/posts/{test_posts[3].id}'
    )

    assert res.status_code == 403


def test_update_post(authorize_client, test_posts):
    res = authorize_client.put(
        f'/posts/{test_posts[0].id}', json={'title': 'updating post', 'content': 'new content'}
    )

    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200 
    assert updated_post.title == 'updating post'
    assert updated_post.content == 'new content'


def test_unauthorized_user_update_post(client, test_posts):
    
    res = client.put(
        f'/posts/{test_posts[0].id}', json={'title': 'updating post', 'content': 'new content'}
    )

    assert res.status_code == 401

def test_update_other_user_post(authorize_client, test_posts):
    res = authorize_client.put(
        f'/posts/{test_posts[3].id}', json={'title': 'updating post', 'content': 'new content'}
    )

    assert res.status_code == 403 


def test_update_non_existing_post(authorize_client):
    res = authorize_client.put(
        f'/posts/{1000000}', json={'title': 'updating post', 'content': 'new content'}
    )

    assert res.status_code == 404


#pytest tests/test_posts.py -v -s
