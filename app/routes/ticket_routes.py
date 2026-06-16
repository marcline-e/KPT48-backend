from fastapi import APIRouter, Depends, HTTPException, status
import pymysql
from datetime import datetime

from app.schemas.ticket_schema import TicketRegisterSchema
from app.database.mysql import get_db
from app.routes.auth_routes import get_current_user

router = APIRouter(prefix="/ticket", tags=["Ticket"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def register_ticket(
    req: TicketRegisterSchema,
    conn: pymysql.connections.Connection = Depends(get_db),
    # Mengambil ID user langsung dari token keamanan, bukan dari input manual
    current_user: dict = Depends(get_current_user) 
):
    id_user = current_user["id_user"]
    cursor = conn.cursor()

    try:
        # 1. MEMULAI TRANSAKSI (Sangat Penting)
        conn.begin()

        # 2. Tarik data Event dan kunci baris (FOR UPDATE)
        cursor.execute("SELECT * FROM events WHERE id_event = %s FOR UPDATE", (req.id_event,))
        event = cursor.fetchone()

        if not event:
            raise HTTPException(status_code=404, detail="Event tidak ditemukan.")

        current_ticket_price = event["ticket_price"]

        # 3. Validasi Timeline Fase Ticketing
        now = datetime.now()
        if req.phase == "OFFICIAL" and not (event["official_open_at"] <= now <= event["official_close_at"]):
            raise HTTPException(status_code=400, detail="Fase Official Ticketing tutup.")
        
        elif req.phase == "GENERAL":
            if not event["general_open_at"] or not event["general_close_at"]:
                raise HTTPException(status_code=400, detail="Jadwal Fase General belum diatur.")
            if not (event["general_open_at"] <= now <= event["general_close_at"]):
                raise HTTPException(status_code=400, detail="Fase General Ticketing tutup.")

        # 4. Validasi Saldo Poin dengan kunci baris (FOR UPDATE)
        cursor.execute("SELECT balance FROM point_balances WHERE id_user = %s FOR UPDATE", (id_user,))
        point_balance = cursor.fetchone()

        if not point_balance or point_balance["balance"] < current_ticket_price:
            raise HTTPException(status_code=400, detail="Saldo poin Anda tidak mencukupi.")

        # 5. Potong saldo
        cursor.execute(
            "UPDATE point_balances SET balance = balance - %s WHERE id_user = %s",
            (current_ticket_price, id_user)
        )

        # 6. Buat Tiket PENDING
        cursor.execute(
            """
            INSERT INTO ticket_registrations (id_user, id_event, phase, status, point_spent) 
            VALUES (%s, %s, %s, 'PENDING', %s)
            """,
            (id_user, req.id_event, req.phase, current_ticket_price)
        )
        ticket_id = cursor.lastrowid

        # 7. Catat transaksi poin
        cursor.execute(
            """
            INSERT INTO point_transactions (id_user, amount, type, reference_id) 
            VALUES (%s, %s, 'deduct', %s)
            """,
            (id_user, -current_ticket_price, ticket_id)
        )

        # 8. Jika semua perintah di atas berhasil, simpan permanen
        conn.commit()

        return {
            "status": "success",
            "message": f"Berhasil mendaftar tiket. Poin terpotong: {current_ticket_price}",
            "ticket_id": ticket_id
        }

    except HTTPException as he:
        # Jika terjadi error validasi logika (saldo kurang, fase tutup), batalkan perubahan database
        conn.rollback()
        raise he
        
    except pymysql.err.Error as e:
        # Jika terjadi error sintaks SQL, batalkan perubahan database
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Transaksi gagal: {str(e)}")
        
    finally:
        cursor.close()