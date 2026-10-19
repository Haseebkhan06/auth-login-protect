
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Response,
    status,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field
from supabase import create_client
from supabase_auth.errors import AuthApiError

from app.auth import get_current_user


# Load environment variables from the project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in .env")


# Initialize Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Auth Login & Protect API")

# Bearer token authentication for Swagger and protected routes
security = HTTPBearer(auto_error=False)


# Request models
class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


# Home endpoint
@app.get("/")
def home():
    return {"message": "Auth Login & Protect API is running"}


# Public endpoint
@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}


# Signup endpoint
@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(data: SignupRequest):
    try:
        result = supabase.auth.sign_up(
            {
                "email": str(data.email),
                "password": data.password,
            }
        )

        if not result.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Signup could not be completed.",
            )

        return {
            "message": (
                "Signup successful. Check your email "
                "if confirmation is required."
            ),
            "user": {
                "id": result.user.id,
                "email": result.user.email,
            },
        }

    except AuthApiError as exc:
        message = str(exc).lower()

        if "already registered" in message or "already exists" in message:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email may already exist.",
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Signup failed. Check your input and Supabase Auth settings.",
        ) from exc


# Login endpoint
@app.post("/auth/login")
def login(data: LoginRequest):
    try:
        result = supabase.auth.sign_in_with_password(
            {
                "email": str(data.email),
                "password": data.password,
            }
        )

        if not result.user or not result.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        return {
            "message": "Login successful",
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token,
            "token_type": "bearer",
            "user": {
                "id": result.user.id,
                "email": result.user.email,
            },
        }

    except AuthApiError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                "Invalid email or password, "
                "or email confirmation is required."
            ),
        ) from exc


# Protected profile endpoint
@app.get("/protected/profile")
def profile(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }




@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user=Depends(get_current_user),
):
    try:
        # Sign out using the SDK's expected options format
        supabase.auth.sign_out({"scope": "global"})

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except AuthApiError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Logout failed",
        ) from exc

