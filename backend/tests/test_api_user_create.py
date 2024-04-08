from flask.testing import FlaskClient


def test_user_create_success(client: FlaskClient):
    user = {'name': 'John Doe'}
