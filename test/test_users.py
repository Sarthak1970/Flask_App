import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import create_app
from pymongo import MongoClient
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://mongo:27017/test_user_db').replace('user_db', 'test_user_db')
    with app.test_client() as client:
        yield client

@pytest.fixture
def clear_db():
    """Clear the test database before each test."""
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongo:27017/test_user_db').replace('user_db', 'test_user_db')
    client = MongoClient(mongo_uri)
    db = client['test_user_db']
    db.users.drop()
    client.close()

@pytest.fixture
def user_id(client, clear_db):
    """Create a user and return its ID."""
    unique_email = f"test{int(time.time())}@example.com"
    user_data = {
        "name": "Test User",
        "email": unique_email,
        "password": "testpassword"
    }
    rv = client.post('/users', json=user_data)
    assert rv.status_code == 201, f"POST /users failed: {rv.get_json()}"
    assert rv.json['status'] == 'success'
    assert rv.json['data']['email'] == user_data['email']
    return rv.json['data']['_id']

def test_get_root(client, clear_db):
    rv = client.get('/')
    assert rv.status_code == 200, f"GET / failed: {rv.get_json()}"
    assert rv.json['message'] == 'Flask User API is running!'

def test_create_user(client, clear_db):
    unique_email = f"test{int(time.time())}@example.com"
    user_data = {
        "name": "Test User",
        "email": unique_email,
        "password": "testpassword"
    }
    rv = client.post('/users', json=user_data)
    assert rv.status_code == 201, f"POST /users failed: {rv.get_json()}"
    assert rv.json['status'] == 'success'
    assert rv.json['data']['email'] == user_data['email']

def test_get_users(client, user_id):
    rv = client.get('/users')
    assert rv.status_code == 200, f"GET /users failed: {rv.get_json()}"
    assert rv.json['status'] == 'success'

def test_get_user_by_id(client, user_id):
    print(f"Testing GET /users/{user_id}")
    rv = client.get(f'/users/{user_id}')
    assert rv.status_code == 200, f"GET /users/{user_id} failed: {rv.get_json()}"
    assert rv.json['status'] == 'success'
    assert rv.json['data']['_id'] == user_id

def test_update_user(client, user_id):
    print(f"Testing PUT /users/{user_id}")
    unique_email = f"updated{int(time.time())}@example.com"
    update_data = {
        "name": "Updated User",
        "email": unique_email,
        "password": "newpassword"
    }
    rv = client.put(f'/users/{user_id}', json=update_data)
    assert rv.status_code == 200, f"PUT /users/{user_id} failed: {rv.get_json()}"
    assert rv.json['status'] == 'success'
    assert rv.json['data']['name'] == update_data['name']
    assert rv.json['data']['email'] == update_data['email']

def test_delete_user(client, user_id):
    print(f"Testing DELETE /users/{user_id}")
    rv = client.delete(f'/users/{user_id}')
    assert rv.status_code == 200, f"DELETE /users/{user_id} failed: {rv.get_json()}"
    assert rv.json['status'] == 'success'
    assert rv.json['data']['message'] == f"User with ID {user_id} deleted"