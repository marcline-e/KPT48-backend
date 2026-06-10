from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.sql_engine import get_db 
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    decode_access_token
)

# 1. Definisi Router
router = APIRouter(tags=["Authentication"])

# 2. Definisi Dependency untuk "Satpam" (OAuth2)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Pindahkan fungsi ini ke atas sini!
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = decode_access_token(token)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User tidak ditemukan")
    return user

# 3. Schemas
class UserLogin(BaseModel):
    email: str
    password: str

# 4. Rute (Routes) - Fungsi ini sekarang aman karena get_current_user sudah dikenal
@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar!")

    hashed_pwd = get_password_hash(user_data.password)
    
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        nik=user_data.nik,
        password_hash=hashed_pwd 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email tidak ditemukan")

    if not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Password salah")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def get_my_profile(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name
    }