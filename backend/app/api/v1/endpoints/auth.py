"""Authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.models.user import User
from app.schemas.token import Token, TokenRefresh
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.auth_service import AuthService

router = APIRouter()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, service: AuthService = Depends(get_auth_service)):
    try:
        return service.register(user_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.post("/login", response_model=Token)
def login(login_in: UserLogin, service: AuthService = Depends(get_auth_service)):
    user = service.authenticate(login_in.email, login_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return service.login_tokens(user)


@router.post("/refresh", response_model=Token)
def refresh(token_in: TokenRefresh, service: AuthService = Depends(get_auth_service)):
    payload = decode_token(token_in.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    user_id = payload.get("sub")
    user = service.users.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return service.login_tokens(user)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
