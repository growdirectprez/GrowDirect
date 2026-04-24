import pytest
from solex import create_app
from solex.config import TestConfig


@pytest.fixture()
def app():
    return create_app(TestConfig)


@pytest.fixture()
def client(app):
    return app.test_client()
