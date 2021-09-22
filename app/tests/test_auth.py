import os
import json
import shutil
import pytest

from fastapi.testclient import TestClient
from fastapi import status

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_cleanup():
    os.makedirs(os.path.join(os.getcwd(), "app", "store"), exist_ok=True)
    if not os.path.exists(os.path.join(os.getcwd(), "app", "store", "users.json")):
        with open(os.path.join(os.getcwd(), "app", "store", "users.json"), "w") as f:
            json.dump({}, f)

    yield

    if os.path.exists(os.path.join(os.getcwd(), "app", "store")):
        shutil.rmtree(os.path.join(os.getcwd(), "app", "store"))


def test_signup():
    res = client.post("/signup", json={"username": "test", "password": "password@1234"})
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["access_token"] is not None


def test_unauthenticated():
    res = client.get("/users/me/")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_auth():
    res = client.post("/signup", json={"username": "test", "password": "password@1234"})
    token = res.json()["access_token"]
    assert token is not None
    res = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == status.HTTP_200_OK
    assert res.json() is not None


def test_disabled():
    res = client.post("/signup", json={"username": "test", "password": "password@1234"})
    token = res.json()["access_token"]

    assert token is not None

    res = client.post(
        "/users/update/",
        headers={"Authorization": f"Bearer {token}"},
        json={"disabled": True},
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() is not None

    res2 = client.get("/users/me")
    assert res2.status_code == status.HTTP_401_UNAUTHORIZED

    res = client.post(
        "/users/update/",
        headers={"Authorization": f"Bearer {token}"},
        json={"disabled": False},
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() is not None

    res2 = client.get("/users/me")
    assert res2.status_code == status.HTTP_401_UNAUTHORIZED
    assert res.json() is not None
