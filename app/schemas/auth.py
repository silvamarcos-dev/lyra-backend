from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


class MeResponse(BaseModel):
    id: int
    name: str
    email: str
    status: str