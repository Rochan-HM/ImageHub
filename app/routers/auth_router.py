from json import load
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from dotenv import load_dotenv

from app.models.auth_model import UserInput, Token, User, UserInDB
from app.middleware.auth import *

load_dotenv()
router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])


@router.post("/signup", tags=["Auth"])
async def signin(user: UserInput):
    user_exists = get_user(user.username)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    with open("./app/store/users.json", "r") as f:
        users = json.load(f)

    users[user.username] = {
        "username": user.username,
        "full_name": user.full_name,
        "disabled": False,
        "email": user.email,
        "hashed_password": get_password_hash(user.password),
    }

    with open("./app/store/users.json", "w") as f:
        json.dump(users, f)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token, tags=["Auth"])
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User, tags=["Auth"])
async def get_logged_in_user(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/users/update/", tags=["Auth"])
async def update_user_status(
    update: UserUpdate, current_user: User = Depends(get_current_user)
):
    with open("./app/store/users.json", "r") as f:
        users = json.load(f)

    users[current_user.username]["disabled"] = update.disable

    with open("./app/store/users.json", "w") as f:
        json.dump(users, f)

    return {"Operation": "Success"}
