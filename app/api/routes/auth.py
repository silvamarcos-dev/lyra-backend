from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, MeResponse
from app.data.repositories.user_repository import (
    get_user_by_email,
    get_user_by_id,
    create_user,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido.")

        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado.")

        return user

    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")


@router.post("/register", response_model=TokenResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, request.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Já existe um usuário com este e-mail.")

    password_hash = hash_password(request.password)

    user = create_user(
        db=db,
        name=request.name,
        email=request.email,
        password_hash=password_hash,
    )

    access_token = create_access_token(subject=user.email, user_id=user.id)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "status": user.status,
        },
    )


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)

    if not user:
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")

    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")

    access_token = create_access_token(subject=user.email, user_id=user.id)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "status": user.status,
        },
    )


@router.get("/me", response_model=MeResponse)
def me(current_user=Depends(get_current_user)):
    return MeResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        status=current_user.status,
    )