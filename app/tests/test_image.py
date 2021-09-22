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
    os.makedirs(
        os.path.join(os.getcwd(), "app", "store", "image"),
        exist_ok=True,
    )
    os.makedirs(
        os.path.join(os.getcwd(), "app", "store", "data"),
        exist_ok=True,
    )
    if not os.path.exists(os.path.join(os.getcwd(), "app", "store", "users.json")):
        with open(os.path.join(os.getcwd(), "app", "store", "users.json"), "w") as f:
            json.dump({}, f)

    yield

    # if os.path.exists(os.path.join(os.getcwd(), "app", "store")):
    #     shutil.rmtree(os.path.join(os.getcwd(), "app", "store"))


def test_unauthorized():
    res = client.get("/images")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert res.json() is not None


def test_upload():
    res = client.post("/signup", json={"username": "test", "password": "password@1234"})
    token = res.json()["access_token"]

    assert token is not None

    res = client.post(
        "/uploadone",
        headers={
            "Authorization": f"Bearer {token}",
        },
        files={
            "file": open(os.path.join(os.getcwd(), "app", "tests", "image.jpg"), "rb")
        },
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() is not None

    image_id = res.json()["id"]

    res = client.get(
        f"/images/{image_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res is not None
