import pytest
from app import create_app, db

def test_app_creation():
    """Test that the Flask app creates successfully"""
    app = create_app()
    assert app is not None
    assert app.config['TESTING'] is False

def test_database_connection():
    """Test database connection and model creation"""
    app = create_app()
    with app.app_context():
        # Test that we can create tables
        db.create_all()
        assert True  # If we reach here, database works

def test_api_endpoints():
    """Test that API endpoints exist"""
    app = create_app()
    with app.test_client() as client:
        response = client.get('/api/test-runs')
        assert response.status_code == 200