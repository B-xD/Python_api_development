from app import schemas
from app import models 
import pytest 

@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id = test_posts[3].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()


def test_votes_on_post(authorize_client, test_posts):
    res = authorize_client.post(
        f'/vote/', 
        json = {'post_id': test_posts[3].id, 'dir': 1}
    )

    assert res.status_code == 201 

def test_votes_twice_posts(authorize_client, test_vote, test_posts):
    res = authorize_client.post(
        f'/vote/', json = {'post_id': test_posts[3].id, 'dir':1} 
    )

    assert res.status_code == 409

def test_delete_vote(authorize_client, test_vote, test_posts):
    res = authorize_client.post(
        f'/vote/', json = {'post_id': test_posts[3].id, 'dir':0}
    
    )

    assert res.status_code == 201

def test_delete_vote_non_exit(authorize_client, test_posts):
    res = authorize_client.post(
        '/vote/', json = {'post_id': test_posts[0].id, 'dir':0}
    )

    assert res.status_code == 404 

def test_vote_post_non_exit(authorize_client, test_posts):
    res = authorize_client.post(
        '/vote/', json = {'post_id': 10000, 'dir':1}
    )

    assert res.status_code == 404 

def test_vote_unauthorized_user(client, test_posts):
    res = client.post(
        '/vote/', json = {'post_id': test_posts[0].id, 'dir':1}
    )

    assert res.status_code == 401
#pytest tests/test_votes.py -v 