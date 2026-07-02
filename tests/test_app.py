"""Tests for the sample Flask application."""


def test_hello(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.data == b"Hello, World!"


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["status"] == "ok"
    assert "time" in body


def test_greet(client):
    resp = client.get("/greet/Ada")
    assert resp.status_code == 200
    assert resp.get_json() == {"message": "Hello, Ada!"}


def test_list_todos_starts_empty(client):
    resp = client.get("/todos")
    assert resp.status_code == 200
    assert resp.get_json() == {"todos": []}


def test_create_todo(client):
    resp = client.post("/todos", json={"title": "write tests"})
    assert resp.status_code == 201
    todo = resp.get_json()["todo"]
    assert todo == {"id": 1, "title": "write tests", "done": False}

    # The created todo should now appear in the list.
    listed = client.get("/todos").get_json()["todos"]
    assert listed == [todo]


def test_create_todo_requires_title(client):
    resp = client.post("/todos", json={})
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "'title' is required"}


def test_todos_are_isolated_between_tests(client):
    # Because each test gets a fresh app, state does not leak.
    assert client.get("/todos").get_json() == {"todos": []}
