from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.mysql import get_db
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
    current_user = Depends(get_current_user)
):
    user_id = current_user["id_user"]
    
    # 1. Cek saldo saat ini
    balance_query = text("SELECT balance FROM point_balances WHERE id_user = :id_user")
    wallet = db.execute(balance_query, {"id_user": user_id}).mappings().first()
    
    if not wallet:
        # Insert dompet baru
        db.execute(text("INSERT INTO point_balances (id_user, balance) VALUES (:id_user, 0)"), {"id_user": user_id})
        current_balance = 0
    else:
        current_balance = wallet["balance"]
    
    new_balance = current_balance + request.amount
    
    # 2. Update saldo
    db.execute(
        text("UPDATE point_balances SET balance = :balance WHERE id_user = :id_user"),
        {"balance": new_balance, "id_user": user_id}
    )
    
    # 3. Catat riwayat
    db.execute(
        text("INSERT INTO point_transactions (id_user, amount, type) VALUES (:id_user, :amount, 'topup')"),
        {"id_user": user_id, "amount": request.amount}
    )
    
    # 4. Simpan semua perubahan ke database (Commit)
    db.commit()
    
    return {
        "success": True,
        "message": f"Berhasil top-up {request.amount} poin!",
        "current_balance": new_balance
    }