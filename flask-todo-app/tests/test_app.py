"""
Basic tests for the Flask Todo App.
"""
import pytest

from app import create_app, db


class TestConfig:
    SECRET_KEY = "test-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True


@pytest.fixture
def app():
    app = create_app(config_object=TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_index_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"My Todo List" in response.data


def test_create_todo_via_api(client):
    response = client.post("/api/todos", json={"title": "Buy milk"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Buy milk"
    assert data["done"] is False


def test_create_todo_requires_title(client):
    response = client.post("/api/todos", json={})
    assert response.status_code == 400


def test_list_todos_via_api(client):
    client.post("/api/todos", json={"title": "Task 1"})
    client.post("/api/todos", json={"title": "Task 2"})
    response = client.get("/api/todos")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


def test_delete_todo_via_api(client):
    create_resp = client.post("/api/todos", json={"title": "Delete me"})
    todo_id = create_resp.get_json()["id"]

    delete_resp = client.delete(f"/api/todos/{todo_id}")
    assert delete_resp.status_code == 200

    list_resp = client.get("/api/todos")
    assert len(list_resp.get_json()) == 0


def test_add_todo_via_form(client):
    response = client.post("/todos", data={"title": "Form task"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Form task" in response.data


def test_toggle_todo(client):
    create_resp = client.post("/api/todos", json={"title": "Toggle me"})
    todo_id = create_resp.get_json()["id"]

    response = client.post(f"/todos/{todo_id}/toggle", follow_redirects=True)
    assert response.status_code == 200
