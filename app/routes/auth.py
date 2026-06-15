from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.mysql import get_db 
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User

# ... (lanjutkan kode fungsi register-mu di bawah)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # 1. Cek apakah email sudah terdaftar
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar!")

    # 2. Buat user baru
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        nik=user_data.nik,
        password_hash=user_data.password # Nanti kita enkripsi ya!
    )
    
    # 3. Simpan ke database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user