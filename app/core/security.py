import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from fastapi import HTTPException, status

SECRET_KEY = "kpt48-rahasia-banget"
ALGORITHM = "HS256"

def get_password_hash(password: str) -> str:
    # Ubah string ke bytes, generate salt, lalu hash
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from fastapi import HTTPException, status # Tambahkan import ini di atas

def decode_access_token(token: str):
    print("\n" + "="*30)
    print(f"DEBUG: Token yang diterima backend:")
    print(token)
    print("="*30 + "\n")
    
    try:
        # Decode token menggunakan SECRET_KEY
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        print(f"DEBUG: Sukses membaca token! Emailnya adalah: {email}")
        if email is None:
            raise HTTPException(status_code=401, detail="Token tidak valid")
        return email
    except jwt.JWTError as e:
        print(f"DEBUG: JWT ERROR! Satpam menolak karena: {e}")
        raise HTTPException(status_code=401, detail="Token tidak valid")