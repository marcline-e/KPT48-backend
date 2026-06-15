from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.ticket_schema import TicketRegisterSchema # Sesuaikan dengan nama file schemamu
from app.database.mysql import get_db
from datetime import datetime
from app.routes.auth_routes import get_current_user # Import get_current_user jika id_user didapat dari token

router = APIRouter()

# Di dalam routes/ticket_routes.py

@router.post("/", status_code=status.HTTP_201_CREATED)
def register_ticket(req: TicketRegisterSchema, id_user: int, db: Session = Depends(get_db)):
    # Jika id_user didapat dari token, gunakan get_current_user:
    # current_user = Depends(get_current_user)
    # 1. Tarik data User
    user_query = text("SELECT id_user FROM users WHERE id_user = :id_user")
    user = db.execute(user_query, {"id_user": id_user}).first()

    if not user:
        # Jangan di-redirect di sini, tapi kirim status 401 agar Frontend tahu user harus daftar/login ulang
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail={
                "error_code": "USER_NOT_FOUND",
                "message": "Akun tidak ditemukan. Silakan lakukan registrasi terlebih dahulu.",
                "action": "REDIRECT_TO_REGISTRATION" # Hint/petunjuk untuk anak Frontend
            }
        )

    # 2. Tarik data Event
    event_query = text("SELECT * FROM events WHERE id_event = :id_event")
    event = db.execute(event_query, {"id_event": req.id_event}).mappings().first()

    if not event:
        raise HTTPException(status_code=404, detail="Event tidak ditemukan.")
        
    current_ticket_price = event["ticket_price"]

    # 3. Validasi Timeline Fase Ticketing
    now = datetime.now()
    if req.phase == "OFFICIAL" and not (event["official_open_at"] <= now <= event["official_close_at"]):
        raise HTTPException(status_code=400, detail="Fase Official Ticketing tutup.")
    elif req.phase == "GENERAL" and not (event["general_open_at"] <= now <= event["general_close_at"]):
        raise HTTPException(status_code=400, detail="Fase General Ticketing tutup.")

    # 4. Validasi Saldo Poin (Pakai variabel harga yang baru)
    balance_query = text("SELECT balance FROM point_balances WHERE id_user = :id_user")
    point_balance = db.execute(balance_query, {"id_user": id_user}).mappings().first()

    if not point_balance or point_balance["balance"] < current_ticket_price:
        raise HTTPException(status_code=400, detail="Saldo poin Anda tidak mencukupi.")

    try:
        # A. Potong saldo
        db.execute(
            text("UPDATE point_balances SET balance = balance - :price, updated_at = :now WHERE id_user = :id_user"),
            {"price": current_ticket_price, "now": now, "id_user": id_user}
        )
        
        # B. Catat transaksi poin
        trans_result = db.execute(
            text("INSERT INTO point_transactions (id_user, amount, type, created_at) VALUES (:id_user, :amount, 'deduct', :now)"),
            {"id_user": id_user, "amount": -current_ticket_price, "now": now}
        )
        trans_id = trans_result.lastrowid
        
        # C. Buat Tiket PENDING
        ticket_result = db.execute(
            text("""
                INSERT INTO ticket_registrations (id_user, id_event, phase, status, point_spent, registered_at) 
                VALUES (:id_user, :id_event, :phase, 'PENDING', :point_spent, :now)
            """),
            {"id_user": id_user, "id_event": req.id_event, "phase": req.phase, "point_spent": current_ticket_price, "now": now}
        )
        ticket_id = ticket_result.lastrowid
        
        # Update reference_id di transaksi poin
        db.execute(
            text("UPDATE point_transactions SET reference_id = :ticket_id WHERE id_point_transaction = :trans_id"),
            {"ticket_id": ticket_id, "trans_id": trans_id}
        )
        
        db.commit()

        return {
            "status": "success",
            "message": f"Berhasil mendaftar war tiket. Poin terpotong: {current_ticket_price}"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Transaksi gagal: {str(e)}")