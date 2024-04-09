from random import randint
from typing import Any

from flask.testing import FlaskClient

from app.entities.user import UserRepository


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

    UserRepository().drop()

    assert res.status_code == 200
    assert (res.json or {})['user']['key'] == user['key']


def test_get_user_not_found(client: FlaskClient):
    res = client.get('/api/users/not-exists')

    UserRepository().drop()

    assert res.status_code == 404
