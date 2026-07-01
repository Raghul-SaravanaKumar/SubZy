from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt

from app.database import db
from app.models import User, LoginRequest
from app.jwt_handler import create_access_token

router = APIRouter()


# ---------------------------
# Register
# ---------------------------
@router.post("/register")
def register(user: User):

    existing_user = db.users.find_one(
        {
            "email": user.email
        }
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = bcrypt.hash(
        user.password
    )

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "created_at": user.created_at
    }

    result = db.users.insert_one(
        new_user
    )

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }


# ---------------------------
# Login
# ---------------------------
@router.post("/login")
def login(data: LoginRequest):

    user = db.users.find_one(
        {
            "email": data.email
        }
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if not bcrypt.verify(
        data.password,
        user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    token = create_access_token(
        str(user["_id"])
    )

    return {
        "message": "Login Successful",
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }
    }