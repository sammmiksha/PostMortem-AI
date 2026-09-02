from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database.dependency import get_db
from app.models.auth import UserRecord
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse, UserResponse
from app.services.auth_service import AuthService
from typing import Optional

router = APIRouter(
    prefix="/auth",
    tags=["Authentication & RBAC"]
)

auth_service = AuthService()

@router.post("/register", response_model=AuthResponse)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    existing = db.query(UserRecord).filter(UserRecord.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = UserRecord(
        name=request.name,
        email=request.email,
        hashed_password=auth_service.hash_password(request.password),
        role=request.role or "Engineer"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = auth_service.create_token(user.id, user.email, user.role)
    return {
        "token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }

@router.post("/login", response_model=AuthResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(UserRecord).filter(UserRecord.email == request.email).first()
    if not user or not auth_service.verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = auth_service.create_token(user.id, user.email, user.role)
    return {
        "token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }

@router.get("/me", response_model=UserResponse)
def get_me(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    token = authorization.replace("Bearer ", "").strip()
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(UserRecord).filter(UserRecord.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }
