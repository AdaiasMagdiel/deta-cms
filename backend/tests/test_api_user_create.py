import pytest
from flask.testing import FlaskClient
from app.repositories.user import User

endpoint = '/api/auth/register'


@pytest.fixture(autouse=True)
def run_after_each_test():
    yield

    User().drop_all()


def test_should_create_user(client: FlaskClient):
    user = {
        'name': 'John Doe',
        'username': 'john.doe',
        'email': 'jhdoe@email.com',
        'password': '123',
        'role': 'ADMIN'
    }

    res = client.post(endpoint, json=user)

    assert res.status_code == 201
    assert 'user' in (res.get_json(silent=True) or {})


def test_is_not_possible_to_create_user_with_missing_data(client: FlaskClient):
    res = client.post(endpoint)

    assert res.status_code == 422


def test_cannot_create_user_with_missing_fields(client: FlaskClient):
    name = client.post(
        endpoint,
        json={
            'username': 'john.doe',
            'email': 'jhdoe@email.com',
            'password': '123',
            'role': 'ADMIN'
        }
    )

    username = client.post(
        endpoint,
        json={
            'name': 'John Doe',
            'email': 'jhdoe@email.com',
            'password': '123',
            'role': 'ADMIN'
        }
    )

    email = client.post(
        endpoint,
        json={
            'name': 'John Doe',
            'username': 'john.doe',
            'password': '123',
            'role': 'ADMIN'
        }
    )

    password = client.post(
        endpoint,
        json={
            'name': 'John Doe',
            'username': 'john.doe',
            'email': 'jhdoe@email.com',
            'role': 'ADMIN'
        }
    )

    role = client.post(
        endpoint,
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


def test_cannot_create_user_with_invalid_username(client: FlaskClient):
    res1 = client.post(
        endpoint,
        json={
            'name': 'John Doe',
            'username': 'john doe',
            'email': 'jhdoe@email.com',
            'password': '123',
            'role': 'ADMIN'
        }
    )
    res2 = client.post(
        endpoint,
        json={
            'name': 'John Doe',
            'username': 'john|doe',
            'email': 'jhdoe@email.com',
            'password': '123',
            'role': 'ADMIN'
        }
    )
    res3 = client.post(
        endpoint,
        json={
            'name': 'John Doe',
            'username': 'johnÁdoe',
            'email': 'jhdoe@email.com',
            'password': '123',
            'role': 'ADMIN'
        }
    )
    res4 = client.post(
        endpoint,
        json={
            'name': 'John Doe',
            'username': 'ab',
            'email': 'jhdoe@email.com',
            'password': '123',
            'role': 'ADMIN'
        }
    )

    assert res1.status_code == 422
    assert res2.status_code == 422
    assert res3.status_code == 422
    assert res4.status_code == 422


def test_cannot_create_user_with_invalid_email(client: FlaskClient):
    res1 = client.post(
        endpoint,
        json={
            'name': 'John Doe',
            'username': 'john doe',
            'email': 'jhdoe email.com',
            'password': '123',
            'role': 'ADMIN'
        }
    )
    res2 = client.post(
        endpoint,
        json={
            'name': 'John Doe',
            'username': 'john|doe',
            'email': 'jhdoe@emailcom',
            'password': '123',
            'role': 'ADMIN'
        }
    )
    res3 = client.post(
        endpoint,
        json={
            'name': 'John Doe',
            'username': 'johnÁdoe',
            'email': 'jhdoe email com',
            'password': '123',
            'role': 'ADMIN'
        }
    )

    assert res1.status_code == 422
    assert res2.status_code == 422
    assert res3.status_code == 422


def test_cannot_create_user_with_used_username_or_used_email(
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

    res_username_1 = client.post(endpoint, json=user_username_1)
    res_username_2 = client.post(endpoint, json=user_username_2)

    res_email_1 = client.post(endpoint, json=user_email_1)
    res_email_2 = client.post(endpoint, json=user_email_2)

    assert res_username_1.status_code == 201
    assert res_username_2.status_code == 409
    assert res_email_1.status_code == 201
    assert res_email_2.status_code == 409


def test_cannot_create_user_with_used_username_username_are_caseinsensitive(
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

    res_username_1 = client.post(endpoint, json=user_username_1)
    res_username_2 = client.post(endpoint, json=user_username_2)

    assert res_username_1.status_code == 201
    assert res_username_2.status_code == 409


def test_cannot_create_user_with_used_email_email_are_caseinsensitive(
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

    res_email_1 = client.post(endpoint, json=user_email_1)
    res_email_2 = client.post(endpoint, json=user_email_2)

    assert res_email_1.status_code == 201
    assert res_email_2.status_code == 409
