from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def get_auth_token():
    """Helper function to get authentication token"""
    response = client.post("/login", json={"username": "demo", "password": "password123"})
    return response.json()["access_token"]

def test_health_check():
    """Test public health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_login_success():
    """Test successful login"""
    response = client.post("/login", json={"username": "demo", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure():
    """Test failed login"""
    response = client.post("/login", json={"username": "demo", "password": "wrong"})
    assert response.status_code == 401

def test_get_items_authenticated():
    """Test getting items with authentication"""
    token = get_auth_token()
    response = client.get("/items", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_get_items_unauthenticated():
    """Test getting items without authentication"""
    response = client.get("/items")
    assert response.status_code == 403

def test_get_item_authenticated():
    """Test getting specific item with authentication"""
    token = get_auth_token()
    response = client.get("/items/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_create_item_authenticated():
    """Test creating item with authentication"""
    token = get_auth_token()
    new_item = {"name": "Test Item", "description": "Test Description", "price": 19.99}
    response = client.post("/items", json=new_item, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"