import pytest
from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models import User
from app.utils.auth_utils import generate_token

@pytest.fixture(scope="function")
def app():
    """Create and configure a clean test application with an in-memory database for each test."""
    application = create_app(TestConfig)
    
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope="function")
def test_user(app):
    """Create a verified test user."""
    with app.app_context():
        user = User(
            name="Alice Engineer",
            email="alice@example.com",
            college="Stanford University",
            branch="Computer Science",
            year=4,
            skills="Python, SQL, System Design",
            is_verified=True
        )
        user.set_password("securepassword123")
        db.session.add(user)
        db.session.commit()
        # Refresh to persist attributes
        user_id = user.user_id
        user_dict = user.to_dict()
        user_dict["user_id"] = user_id
        return user_dict

@pytest.fixture(scope="function")
def auth_headers(test_user):
    """Generate JWT authorization headers for the verified test user."""
    token = generate_token(test_user["user_id"])
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
