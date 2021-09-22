import os
import shutil
import uuid
import json
import glob
import pathlib
import io
import zipfile
from typing import List
from fastapi import APIRouter, UploadFile, File, status, Depends
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from starlette.responses import FileResponse


from app.models.auth_model import User
from app.middleware.auth import *


router = APIRouter()


@router.on_event("startup")
async def setup():
    os.makedirs(os.path.dirname("./app/store/image/"), exist_ok=True)
    os.makedirs(os.path.dirname("./app/store/data/"), exist_ok=True)


@router.get("/images", tags=["Get Images"])
async def get_all_images(current_user: User = Depends(get_current_active_user)):
    ans = []
    for res in glob.iglob("./app/store/data/*.json"):
        with open(res, "r") as f:
            data = json.load(f)

        if data["author"] == current_user.username:
            ans.append(f"./app/store/image/{pathlib.Path(res).stem}.jpg")

    zip_io = io.BytesIO()
    with zipfile.ZipFile(
        zip_io, mode="w", compression=zipfile.ZIP_DEFLATED
    ) as temp_zip:
        for fpath in ans:
            fdir, fname = os.path.split(fpath)
            temp_zip.write(fpath, fname)
    return StreamingResponse(
        iter([zip_io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename=images.zip"},
    )


@router.get("/images/{id}", tags=["Get Images"])
async def get_single_images(
    id: str, current_user: User = Depends(get_current_active_user)
):
    if not os.path.exists(f"./app/store/image/{id}.jpg"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    with open(f"./app/store/data/{id}.json", "r") as f:
        data = json.load(f)
        if data["author"] != current_user.username:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return FileResponse(os.path.join(os.getcwd(), "app", "store", "image", f"{id}.jpg"))


@router.post("/uploadmany", tags=["Upload Multiple Files"])
async def upload_many(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_active_user),
):
    # Since we do not have a database, we just store in file system.
    # However, it would be better to store this in a database for latency and organization.
    try:
        for file in files:

            file_name = str(uuid.uuid4())

            with open(f"./app/store/image/{file_name}.jpg", "wb") as buf:
                shutil.copyfileobj(file.file, buf)

            with open(f"./app/store/data/{file_name}.json", "w") as f:
                json.dump(
                    {"filename": file.filename, "author": current_user.username}, f
                )

        return {"Status": "OK", "id": file_name}

    except Exception as e:
        print(e)
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Corrupt File Received",
        )


@router.post("/uploadone", tags=["Upload One File"])
async def upload_one(
    file: UploadFile = File(...), current_user: User = Depends(get_current_active_user)
):
    try:
        file_name = str(uuid.uuid4())

        with open(f"./app/store/image/{file_name}.jpg", "wb") as buf:
            shutil.copyfileobj(file.file, buf)

        with open(f"./app/store/data/{file_name}.json", "w") as f:
            json.dump({"filename": file.filename, "author": current_user.username}, f)

        return {"Status": "OK", "id": file_name}

    except Exception as e:
        print(e)
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Corrupt File Received",
        )
