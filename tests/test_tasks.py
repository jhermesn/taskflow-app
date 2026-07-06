import app.main as m
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_state():
    m._tasks.clear()
    m._next_id = 1
    yield


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_list_tasks_empty():
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.json() == []


def test_list_tasks():
    client.post("/tasks", json={"title": "a"})
    client.post("/tasks", json={"title": "b"})
    r = client.get("/tasks")
    assert r.status_code == 200
    tasks = r.json()
    assert len(tasks) == 2
    assert {t["title"] for t in tasks} == {"a", "b"}


def test_create_task():
    r = client.post("/tasks", json={"title": "estudar Terraform"})
    assert r.status_code == 201
    task = r.json()
    assert task["id"] == 1
    assert task["title"] == "estudar Terraform"
    assert task["done"] is False


def test_get_task():
    client.post("/tasks", json={"title": "estudar Go"})
    r = client.get("/tasks/1")
    assert r.status_code == 200
    assert r.json()["title"] == "estudar Go"


def test_get_task_not_found():
    r = client.get("/tasks/99")
    assert r.status_code == 404


def test_update_task():
    client.post("/tasks", json={"title": "push to main"})
    r = client.patch("/tasks/1", json={"done": True})
    assert r.status_code == 200
    body = r.json()
    assert body["done"] is True
    assert body["title"] == "push to main"


def test_update_task_not_found():
    r = client.patch("/tasks/99", json={"title": "x", "done": False})
    assert r.status_code == 404


def test_delete_task():
    client.post("/tasks", json={"title": "deletar"})
    r = client.delete("/tasks/1")
    assert r.status_code == 204
    assert client.get("/tasks/1").status_code == 404


def test_delete_task_not_found():
    r = client.delete("/tasks/99")
    assert r.status_code == 404


def test_stats():
    client.post("/tasks", json={"title": "a", "done": True})
    client.post("/tasks", json={"title": "b", "done": False})
    r = client.get("/stats")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert data["done"] == 1  # falha: endpoint retorna 2 (contando todas as tasks)
