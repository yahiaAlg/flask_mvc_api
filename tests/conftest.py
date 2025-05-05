"""
Pytest configuration
"""
import pytest
from app import create_app


@pytest.fixture
def app():
    """Create the Flask app for testing"""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    """Create a test client"""
    with app.test_client() as client:
        yield client