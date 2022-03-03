from http import client
from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Welcome to my api'
    assert res.status_code == 200


def test_create_user():
    res = client.post("/users/", json={"email": "test@example.com", "password": "password123"})
    assert res.status_code == 201
    assert res.json().get("email") == "test@example.com"