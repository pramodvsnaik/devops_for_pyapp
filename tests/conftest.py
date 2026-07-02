"""Shared pytest fixtures for the Flask sample app."""
import pytest

from app import create_app


@pytest.fixture
def app():
    """A fresh app instance in testing mode for each test."""
    application = create_app({"TESTING": True})
    yield application


@pytest.fixture
def client(app):
    """A Flask test client backed by a fresh app."""
    return app.test_client()
