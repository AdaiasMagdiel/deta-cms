import pytest
from flask.testing import FlaskClient
from app.repositories.user import User
from app.repositories.role import Role
from app.utils import slugify

endpoint = '/api/role'


@pytest.fixture(autouse=True)
def run_after_each_test():
    yield

    User().drop_all()
    Role().drop_all()


def test_should_create_role(client: FlaskClient):
    role = {'title': 'Admin'}

    res = client.post(endpoint, json=role)
    data = res.get_json(silent=True) or {}

    assert res.status_code == 201
    assert 'title' in data
    assert 'slug' in data
    assert data['title'] == role['title']
    assert data['slug'] == slugify(role['title'])

    # ---

    role = {'title': 'Guest', 'slug': 'sample-slug'}

    res = client.post(endpoint, json=role)
    data = res.get_json(silent=True) or {}

    assert res.status_code == 201
    assert 'title' in data
    assert 'slug' in data
    assert data['title'] == role['title']
    assert data['slug'] == role['slug']


def test_should_not_create_role_with_existent_title_or_slug(
    client: FlaskClient
):
    role_1 = {'title': 'Admin'}
    role_2 = {'title': 'Admin', 'slug': 'abc'}

    res_1 = client.post(endpoint, json=role_1)
    res_2 = client.post(endpoint, json=role_2)

    assert res_1.status_code == 201
    assert res_2.status_code == 409

    # ---

    role_1 = {'title': 'Ghost', 'slug': '123'}
    role_2 = {'title': 'Guest', 'slug': '123'}

    res_1 = client.post(endpoint, json=role_1)
    res_2 = client.post(endpoint, json=role_2)

    assert res_1.status_code == 201
    assert res_2.status_code == 409

    # ---

    role_1 = {'title': 'Writer'}
    role_2 = {'title': 'Writer'}

    res_1 = client.post(endpoint, json=role_1)
    res_2 = client.post(endpoint, json=role_2)

    assert res_1.status_code == 201
    assert res_2.status_code == 409


def test_should_not_create_role_with_missing_data(client: FlaskClient):
    res_1 = client.post(endpoint)
    assert res_1.status_code == 422

    res_2 = client.post(endpoint, json={'title': ''})
    assert res_2.status_code == 422

    res_3 = client.post(endpoint, json={'title': '', 'slug': ''})
    assert res_3.status_code == 422


def test_should_create_a_slug_for_empty_slugs(client: FlaskClient):
    role = {'title': 'Admin', 'slug': ''}
    res = client.post(endpoint, json=role)
    data = res.get_json(silent=True) or {}

    assert res.status_code == 201
    assert 'slug' in data
    assert data['slug'] == slugify(role['title'])


def test_user_registration_should_create_a_role(client: FlaskClient):
    User().drop_all()
    Role().drop_all()

    assert Role().count() == 0

    user = {
        'name': 'John Doe',
        'username': 'john.doe',
        'email': 'jhdoe@email.com',
        'password': '123',
        'role': 'Admin'
    }

    res = client.post('/api/auth/register', json=user)
    data = (res.get_json(silent=True) or {})

    assert res.status_code == 201
    assert 'role' in data['user']

    assert Role().count() == 1
    assert Role().get_by('title', 'Admin') is not None
    assert 'slug' in data['user']['role']


def test_user_registration_should_can_select_a_existent_role(
    client: FlaskClient
):
    User().drop_all()
    Role().drop_all()
    assert Role().count() == 0

    role_data = {'title': 'Guest'}
    Role().create(role_data)
    assert Role().count() == 1

    user = {
        'name': 'John Doe',
        'username': 'john.doe',
        'email': 'jhdoe@email.com',
        'password': '123',
        'role': 'guesT'  # The search for roles should be case-insensitive
    }

    res = client.post('/api/auth/register', json=user)
    data = (res.get_json(silent=True) or {})

    assert res.status_code == 201
    assert 'role' in data['user']

    assert Role().count() == 1
    assert 'slug' in data['user']['role']
    assert data['user']['role']['title'] == role_data['title']
