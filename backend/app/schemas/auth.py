from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: str = Field(...)
    password: str = Field(..., min_length=6)
    role: Optional[str] = "Engineer"

class LoginRequest(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

class AuthResponse(BaseModel):
    token: str
    user: UserResponse
