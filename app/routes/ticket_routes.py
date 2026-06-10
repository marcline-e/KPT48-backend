from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Event, PointBalance, PointTransaction, TicketRegistration, User
from schemas import TicketRegisterSchema
from database import get_db
from datetime import datetime

router = APIRouter()

# Di dalam routes/ticket_routes.py

@router.post("/ticket/register", status_code=status.HTTP_201_CREATED)
def register_ticket(req: TicketRegisterSchema, id_user: int, db: Session = Depends(get_db)):
    
    # 1. Tarik data User
    user = db.query(User).filter(User.id_user == id_user).first()

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
    event = db.query(Event).filter(Event.id_event == req.id_event).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event tidak ditemukan.")
        
    # =============== DYNAMIC PRICE POINT ===============
    # Sekarang kita pakai harga yang ditentukan admin untuk event ini
    current_ticket_price = event.ticket_price 
    # ===================================================

    # 3. Validasi Timeline Fase Ticketing
    now = datetime.now()
    if req.phase == "OFFICIAL" and not (event.official_open_at <= now <= event.official_close_at):
        raise HTTPException(status_code=400, detail="Fase Official Ticketing tutup.")
    elif req.phase == "GENERAL" and not (event.general_open_at <= now <= event.general_close_at):
        raise HTTPException(status_code=400, detail="Fase General Ticketing tutup.")

    # 4. Validasi Saldo Poin (Pakai variabel harga yang baru)
    point_balance = db.query(PointBalance).filter(PointBalance.id_user == id_user).first()
    if not point_balance or point_balance.balance < current_ticket_price:
        raise HTTPException(status_code=400, detail="Saldo poin Anda tidak mencukupi.")

    try:
        # EXECUTE TRANSACTION (ACID)
        
        # A. Potong saldo sesuai harga tiket event tersebut
        point_balance.balance -= current_ticket_price
        point_balance.updated_at = now
        
        # B. Catat transaksi poin
        point_transaction = PointTransaction(
            id_user=id_user,
            amount=-current_ticket_price, # Minus artinya saldo keluar
            type="deduct",
            created_at=now
        )
        db.add(point_transaction)
        
        # C. Buat Tiket PENDING
        new_ticket = TicketRegistration(
            id_user=id_user,
            id_event=req.id_event,
            attendee_name=user.full_name,
            phase=req.phase,
            status="PENDING",
            point_spent=current_ticket_price, # Rekam berapa poin yang di-spend untuk tiket ini
            registered_at=now
        )
        db.add(new_ticket)
        
        db.commit()
        db.refresh(new_ticket)
        
        point_transaction.reference_id = new_ticket.id_ticket_registration
        db.commit()

        return {
            "status": "success",
            "message": f"Berhasil mendaftar war tiket. Poin terpotong: {current_ticket_price}"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Transaksi gagal: {str(e)}")