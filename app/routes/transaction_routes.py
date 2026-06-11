from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.sql_engine import get_db
from app.models.user import User
from app.models.transaction import PointBalance, PointTransaction
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
    # 1. Cek apakah user sudah punya dompet (PointBalance) di database
    wallet = db.query(PointBalance).filter(PointBalance.user_id == current_user.id).first()
    
    # Kalau belum punya, kita buatkan dompet baru dengan saldo awal 0
    if not wallet:
        wallet = PointBalance(user_id=current_user.id, balance=0)
        db.add(wallet)
    
    # 2. Tambahkan saldo sesuai request
    wallet.balance += request.amount
    
    # 3. Catat riwayat transaksi di PointTransaction
    transaction_log = PointTransaction(
        user_id=current_user.id,
        amount=request.amount,
        transaction_type="TOPUP"
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