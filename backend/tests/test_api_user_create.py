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

    UserRepository().drop()
    assert res.status_code == 201
    assert 'user' in (res.get_json(silent=True) or {})


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


def test_user_cannot_create_with_invalid_username(client: FlaskClient):
    res1 = client.post(
        '/api/users',
        json={
            'name': 'John Doe',
            'username': 'john doe',
            'email': 'jhdoe@email.com',
            'password': '123',
            'role': 'ADMIN'
        }
    )
    res2 = client.post(
        '/api/users',
        json={
            'name': 'John Doe',
            'username': 'john|doe',
            'email': 'jhdoe@email.com',
            'password': '123',
            'role': 'ADMIN'
        }
    )
    res3 = client.post(
        '/api/users',
        json={
            'name': 'John Doe',
            'username': 'johnÁdoe',
            'email': 'jhdoe@email.com',
            'password': '123',
            'role': 'ADMIN'
        }
    )

    UserRepository().drop()
    assert res1.status_code == 422
    assert res2.status_code == 422
    assert res3.status_code == 422


def test_user_cannot_create_with_invalid_email(client: FlaskClient):
    res1 = client.post(
        '/api/users',
        json={
            'name': 'John Doe',
            'username': 'john doe',
            'email': 'jhdoe email.com',
            'password': '123',
            'role': 'ADMIN'
        }
    )
    res2 = client.post(
        '/api/users',
        json={
            'name': 'John Doe',
            'username': 'john|doe',
            'email': 'jhdoe@emailcom',
            'password': '123',
            'role': 'ADMIN'
        }
    )
    res3 = client.post(
        '/api/users',
        json={
            'name': 'John Doe',
            'username': 'johnÁdoe',
            'email': 'jhdoe email com',
            'password': '123',
            'role': 'ADMIN'
        }
    )

    UserRepository().drop()
    assert res1.status_code == 422
    assert res2.status_code == 422
    assert res3.status_code == 422


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

    UserRepository().drop()
    assert res_username_1.status_code == 201
    assert res_username_2.status_code == 422
    assert res_email_1.status_code == 201
    assert res_email_2.status_code == 422


def test_user_cannot_create_with_used_username_username_are_caseinsensitive(
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
        'username': 'JOHN.DOE',
        'email': 'jhdoe2@email.com',
        'password': '123',
        'role': 'ADMIN'
    }

    res_username_1 = client.post('/api/users', json=user_username_1)
    res_username_2 = client.post('/api/users', json=user_username_2)

    UserRepository().drop()
    assert res_username_1.status_code == 201
    assert res_username_2.status_code == 422


def test_user_cannot_create_with_used_email_email_are_caseinsensitive(
    client: FlaskClient
):
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
        'email': 'JHDOE@EMAIL.COM',
        'password': '123',
        'role': 'ADMIN'
    }

    res_email_1 = client.post('/api/users', json=user_email_1)
    res_email_2 = client.post('/api/users', json=user_email_2)

    UserRepository().drop()
    assert res_email_1.status_code == 201
    assert res_email_2.status_code == 422
