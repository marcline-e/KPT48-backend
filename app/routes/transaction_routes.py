from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.sql_engine import get_db
from app.models.user import User
from app.models.point_balance import Point_Balance
from app.models.point_transaction import Point_Transaction
from app.schemas.transaction_schema import TopUpRequest

# PENTING: Import satpam kita dari auth_routes!
from app.routes.auth_routes import get_current_user 

router = APIRouter(tags=["Transaction"])

@router.post("/topup")
def topup_points(
    request: TopUpRequest, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user) # Gembok terpasang di sini!
):
    # 1. Gunakan id_user sesuai dengan model Point_Balance
    wallet = db.query(Point_Balance).filter(Point_Balance.id_user == current_user.id_user).first()
    
    # Kalau belum punya, kita buatkan dompet baru dengan saldo awal 0
    if not wallet:
        wallet = Point_Balance(id_user=current_user.id_user, balance=0)
        db.add(wallet)
    
    # 2. Tambahkan saldo sesuai request
    wallet.balance += request.amount
    
    # 3. Catat riwayat transaksi (Gunakan id_user dan type sesuai model Point_Transaction)
    transaction_log = Point_Transaction(
        id_user=current_user.id_user,
        amount=request.amount,
        type="topup"  # Mengikuti standar penamaan temanmu di komentar file model
    )
    db.add(transaction_log)
    
    # 4. Simpan semua perubahan ke database (Commit)
    db.commit()
    db.refresh(wallet)
    
    return {
        "success": True,
        "message": f"Berhasil top-up {request.amount} poin!",
        "current_balance": wallet.balance
    }