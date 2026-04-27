import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_todos_empty(client):
    res = client.get("/todos")
    assert res.status_code == 200
    assert res.get_json() == []

def test_add_todo(client):
    res = client.post("/todos", json={"task": "Buy milk"})
    assert res.status_code == 201
    assert res.get_json()["task"] == "Buy milk"