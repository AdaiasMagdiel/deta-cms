from random import randint
from typing import Any
from flask.testing import FlaskClient
import pytest
from werkzeug.test import TestResponse
from app.entities.user import UserRepository


@pytest.fixture(autouse=True)
def run_after_each_test():
    yield

    UserRepository().drop()


def get_json(res: TestResponse) -> dict[str, Any]:
    return (res.get_json(silent=True) or {})


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
    data = get_json(res)

    return data.get('user', {})


def test_user_can_update_success(client: FlaskClient):
    user = create_user(client)

    data = {'name': 'New Name'}
    res = client.put(f'/api/users/{user["key"]}', json=data)

    assert res.status_code == 200
    assert get_json(res).get('name', '') == data.get('name', '')

    data = {'password': '456'}
    res = client.put(f'/api/users/{user["key"]}', json=data)

    assert res.status_code == 200

    data = {'username': 'new.username'}
    res = client.put(f'/api/users/{user["key"]}', json=data)

    assert res.status_code == 200
    assert get_json(res).get('username', '') == data.get('username', '')

    data = {'role': 'WRITER'}
    res = client.put(f'/api/users/{user["key"]}', json=data)

    assert res.status_code == 200
    assert get_json(res).get('role', '') == data.get('role', '')

    data = {'email': 'new@email.com'}
    res = client.put(f'/api/users/{user["key"]}', json=data)

    assert res.status_code == 200
    assert get_json(res).get('email', '') == data.get('email', '')


def test_user_cannot_update_with_invalid_key(client: FlaskClient):
    data = {'username': 'new.username'}
    res1 = client.put('/api/users/not-exists', json=data)

    assert res1.status_code == 404


def test_user_cannot_update_with_used_username(client: FlaskClient):
    user = create_user(client)

    data = {'username': user['username']}
    res1 = client.put(f'/api/users/{user["key"]}', json=data)

    data = {'username': user['username'].upper()}
    res2 = client.put(f'/api/users/{user["key"]}', json=data)

    assert res1.status_code == 422
    assert res2.status_code == 422


def test_user_cannot_update_with_used_email(client: FlaskClient):
    user = create_user(client)

    data = {'email': user['email']}
    res1 = client.put(f'/api/users/{user["key"]}', json=data)

    data = {'email': user['email'].upper()}
    res2 = client.put(f'/api/users/{user["key"]}', json=data)

    assert res1.status_code == 422
    assert res2.status_code == 422
