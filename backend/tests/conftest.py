import pytest
from typing import Generator
from flask import Flask
from flask.testing import FlaskClient
from app import create_app

app_ = create_app()
app_.config.update({
    "TESTING": True,
})


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    yield app_


@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()
