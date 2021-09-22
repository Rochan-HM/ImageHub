from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_path():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() is not None
