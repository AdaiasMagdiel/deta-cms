from random import randint
from typing import Any
from flask.testing import FlaskClient
import pytest
from app.entities.user import UserRepository


@pytest.fixture(autouse=True)
def run_after_each_test():
    yield

    UserRepository().drop()


def create_user(client: FlaskClient) -> dict[str, Any]:
    num = randint(1, 1_000)

    user = {
        'name': f'John Doe {num}',
        'username': f'john{num}doe',
        'email': f'jhdoe{num}@email.com',
        'password': '123',
        'role': 'ADMIN'
    }

    res = client.post('/api/users', json=user)
    data = res.get_json(silent=True) or {}

    return data.get('user', {})


def test_get_user(client: FlaskClient):
    user = create_user(client)

    res = client.get(f'/api/users/{user["key"]}')

    assert res.status_code == 200
    assert (res.json or {})['user']['key'] == user['key']


def test_get_user_not_found(client: FlaskClient):
    res = client.get('/api/users/not-exists')

    assert res.status_code == 404


def test_get_pagination(client: FlaskClient):
    # total users: 10
    for i in range(10):
        create_user(client)

    res = client.get('/api/users')  # default per page: 20
    data = res.json or {}

    assert res.status_code == 200
    assert len(data['users']) == 10
    assert data['last_page'] is True

    # total users: 21
    for i in range(11):
        create_user(client)

    res = client.get('/api/users')  # default per page: 20
    data = res.json or {}

    assert res.status_code == 200
    assert len(data['users']) == 20
    assert data['last_page'] is False

    res = client.get('/api/users?page=2')
    data = res.json or {}

    assert res.status_code == 200
    assert len(data['users']) == 1
    assert data['last_page'] is True
