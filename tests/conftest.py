import pytest

from app import create_app
from src.services.demo_data import store


@pytest.fixture()
def app():
    application = create_app()
    application.config.update(TESTING=True)
    store.reset()
    yield application
    store.reset()


@pytest.fixture()
def client(app):
    return app.test_client()
