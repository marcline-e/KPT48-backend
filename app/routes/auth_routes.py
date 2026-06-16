from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import pymysql

from app.database.mysql import get_db 
from app.schemas.user_schema import UserCreate, UserResponse
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    decode_access_token
)

# 1. Definisi Router
router = APIRouter(tags=["Authentication"])

# 2. Definisi Dependency untuk "Satpam" (Menggunakan HTTPBearer)
security_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme), 
    conn: pymysql.connections.Connection = Depends(get_db)
):
    # HTTPBearer otomatis mengambil token dari header "Authorization: Bearer <token>"
    token = credentials.credentials
    email = decode_access_token(token)
    
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    
    if not user:
        raise HTTPException(status_code=401, detail="User tidak ditemukan")
    return user

# 3. Schemas
class UserLogin(BaseModel):
    email: str
    password: str

# 4. Rute (Routes)
@router.post("/register", response_model=UserResponse)
def register_user(
    user_data: UserCreate, 
    conn: pymysql.connections.Connection = Depends(get_db)
):
    cursor = conn.cursor()
    check_query = "SELECT email FROM users WHERE email = %s"
    cursor.execute(check_query, (user_data.email,))
    db_user = cursor.fetchone()
    
    if db_user:
        cursor.close()
        raise HTTPException(status_code=400, detail="Email sudah terdaftar!")

    hashed_pwd = get_password_hash(user_data.password)
    
    insert_query = """
        INSERT INTO users (email, username, full_name, nik, password_hash)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor.execute(insert_query, (
        user_data.email,
        user_data.username,
        user_data.full_name,
        user_data.nik,
        hashed_pwd
    ))
    conn.commit()

    new_id = cursor.lastrowid
    cursor.close()
    
    return {
        "id_user": new_id,
        "email": user_data.email,
        "username": user_data.username,
        "role": "GENERAL"
    }

@router.post("/login")
def login(
    user_credentials: UserLogin, 
    conn: pymysql.connections.Connection = Depends(get_db)
):
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (user_credentials.email,))
    user = cursor.fetchone()
    cursor.close()
    
    if not user:
        raise HTTPException(status_code=404, detail="Email tidak ditemukan")

    if not verify_password(user_credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Password salah")

    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", dependencies=[Depends(security_scheme)])
def get_my_profile(current_user=Depends(get_current_user)):
    return {
        "email": current_user["email"],
        "username": current_user["username"],
        "full_name": current_user["full_name"],
        "role": current_user["role"]
    }