import pytest
from typing import Generator
from flask import Flask
from flask.testing import FlaskClient
from app import create_app


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()
