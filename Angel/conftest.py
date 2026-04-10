"""pytest fixtures for Angel tests.

Provides app factory, test client, authenticated client, and database session.

Note: Angel code actually lives in Cove (Angel is a Cove module).
Real tests run against Cove fixtures in ~/GrowDirect/Cove/conftest.py.
This file provided for scaffolding reference.
"""

import pytest
from angel import create_app, db
from angel.models.lead import Lead


@pytest.fixture
def app():
    """Create and configure a test app."""
    app = create_app("test")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """Database session."""
    with app.app_context():
        yield db.session


@pytest.fixture
def sample_lead(db_session):
    """Create a sample lead for testing."""
    lead = Lead(
        apn="123-456-789",
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        phone="555-0123",
        interest_type="buying",
        message="Interested in the Palos Verdes area",
        page_url="https://angeliquelyle.com/homes",
        status="new",
    )
    db_session.add(lead)
    db_session.commit()
    return lead
