from flask.testing import FlaskClient
from app.entities.user import UserRepository


def test_user_create_success(client: FlaskClient):
    user = {
        'name': 'John Doe',
        'username': 'john.doe',
        'email': 'jhdoe@email.com',
        'password': '123',
        'role': 'ADMIN'
    }

    res = client.post('/api/users', json=user)

    assert res.status_code == 201

    UserRepository().drop()


def test_user_create_missing_data(client: FlaskClient):
    res = client.post('/api/users')

    assert res.status_code == 422


def test_user_cannot_create_with_missing_fields(client: FlaskClient):
    name = client.post(
        '/api/users',
        json={
            'username': 'john.doe',
            'email': 'jhdoe@email.com',
            'password': '123',
            'role': 'ADMIN'
        }
    )

    username = client.post(
        '/api/users',
        json={
            'name': 'John Doe',
            'email': 'jhdoe@email.com',
            'password': '123',
            'role': 'ADMIN'
        }
    )

    email = client.post(
        '/api/users',
        json={
            'name': 'John Doe',
            'username': 'john.doe',
            'password': '123',
            'role': 'ADMIN'
        }
    )

    password = client.post(
        '/api/users',
        json={
            'name': 'John Doe',
            'username': 'john.doe',
            'email': 'jhdoe@email.com',
            'role': 'ADMIN'
        }
    )

    role = client.post(
        '/api/users',
        json={
            'name': 'John Doe',
            'username': 'john.doe',
            'email': 'jhdoe@email.com',
            'password': '123'
        }
    )

    assert name.status_code == 422
    assert username.status_code == 422
    assert email.status_code == 422
    assert password.status_code == 422
    assert role.status_code == 422


def test_user_cannot_create_with_used_username_or_used_email(
    client: FlaskClient
):
    user_username_1 = {
        'name': 'John Doe',
        'username': 'john.doe',
        'email': 'jhdoe1@email.com',
        'password': '123',
        'role': 'ADMIN'
    }
    user_username_2 = {
        'name': 'John Doe',
        'username': 'john.doe',
        'email': 'jhdoe2@email.com',
        'password': '123',
        'role': 'ADMIN'
    }

    user_email_1 = {
        'name': 'John Doe',
        'username': 'john.doe1',
        'email': 'jhdoe@email.com',
        'password': '123',
        'role': 'ADMIN'
    }
    user_email_2 = {
        'name': 'John Doe',
        'username': 'john.doe2',
        'email': 'jhdoe@email.com',
        'password': '123',
        'role': 'ADMIN'
    }

    res_username_1 = client.post('/api/users', json=user_username_1)
    res_username_2 = client.post('/api/users', json=user_username_2)

    res_email_1 = client.post('/api/users', json=user_email_1)
    res_email_2 = client.post('/api/users', json=user_email_2)

    assert res_username_1.status_code == 201
    assert res_username_2.status_code == 422
    assert res_email_1.status_code == 201
    assert res_email_2.status_code == 422

    UserRepository().drop()
