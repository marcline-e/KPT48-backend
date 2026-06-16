from fastapi import APIRouter, Depends, HTTPException, status
import pymysql
from datetime import datetime
import random  # Ditambahkan untuk fungsi acak algoritma gacha

from app.schemas.ticket_schema import TicketRegisterSchema
from app.database.mysql import get_db
from app.routes.auth_routes import get_current_user

router = APIRouter(prefix="/ticket", tags=["Ticket"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def register_ticket(
    req: TicketRegisterSchema,
    conn: pymysql.connections.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user) 
):
    id_user = current_user["id_user"]
    phase = current_user["role"]
    cursor = conn.cursor()

    if current_user["role"] == "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin tidak memiliki akses untuk membeli tiket."
        )

    try:
        conn.begin()

        cursor.execute("SELECT * FROM events WHERE id_event = %s FOR UPDATE", (req.id_event,))
        event = cursor.fetchone()

        if not event:
            raise HTTPException(status_code=404, detail="Event tidak ditemukan.")

        current_ticket_price = event["ticket_price"]

        now = datetime.now()
        user_role = current_user["role"].upper()
        phase_terpilih = None

        if user_role == "OFFICIAL":
            if event["official_open_at"] <= now <= event["official_close_at"]:
                phase_terpilih = "OFFICIAL"
            else:
                raise HTTPException(
                    status_code=400, 
                    detail="Fase pendaftaran khusus Official Member sedang tidak aktif atau sudah ditutup."
                )
        
        elif user_role == "GENERAL":
            if not event["general_open_at"] or not event["general_close_at"]:
                raise HTTPException(status_code=400, detail="Jadwal Fase General belum diatur.")
            if event["general_open_at"] <= now <= event["general_close_at"]:
                phase_terpilih = "GENERAL"
            else:
                raise HTTPException(
                    status_code=400, 
                    detail="Fase pendaftaran General Member belum dibuka atau sudah ditutup."
                )
        else:
            raise HTTPException(status_code=403, detail="Role tidak dikenali.")

        cursor.execute("SELECT balance FROM point_balances WHERE id_user = %s FOR UPDATE", (id_user,))
        point_balance = cursor.fetchone()

        if not point_balance or point_balance["balance"] < current_ticket_price:
            raise HTTPException(status_code=400, detail="Saldo poin Anda tidak mencukupi.")

        cursor.execute(
            "UPDATE point_balances SET balance = balance - %s WHERE id_user = %s",
            (current_ticket_price, id_user)
        )

        cursor.execute(
            """
            INSERT INTO ticket_registrations (id_user, id_event, phase, status, point_spent) 
            VALUES (%s, %s, %s, 'PENDING', %s)
            """,
            (id_user, req.id_event, phase_terpilih, current_ticket_price)
        )
        ticket_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO point_transactions (id_user, amount, type, reference_id) 
            VALUES (%s, %s, 'deduct', %s)
            """,
            (id_user, -current_ticket_price, ticket_id)
        )

        conn.commit()

        return {
            "status": "success",
            "message": f"Berhasil mendaftar tiket. Poin terpotong: {current_ticket_price}",
            "ticket_id": ticket_id
        }

    except HTTPException as he:
        conn.rollback()
        raise he
        
    except pymysql.err.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Transaksi gagal: {str(e)}")
        
    finally:
        cursor.close()

@router.get("/status", status_code=status.HTTP_200_OK)
def check_ticket_status(
    conn: pymysql.connections.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    id_user = current_user["id_user"]
    cursor = conn.cursor()

    try:
        sql = """
            SELECT * FROM ticket_registrations 
            WHERE id_user = %s 
            ORDER BY created_at DESC
        """
        cursor.execute(sql, (id_user,))
        tickets = cursor.fetchall()

        if not tickets:
            return {
                "success": True,
                "message": "Kamu belum mendaftar tiket untuk event apa pun.",
                "data": []
            }

        return {
            "success": True,
            "message": "Status tiket berhasil diambil!",
            "data": tickets
        }

    except pymysql.err.Error as e:
        raise HTTPException(status_code=500, detail=f"Database execution error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        cursor.close()

@router.post("/{id_event}/refund", status_code=status.HTTP_200_OK)
def process_refund(
    id_event: int,
    conn: pymysql.connections.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Hanya Admin yang memiliki akses untuk memproses refund."
        )

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        conn.begin()

        cursor.execute("""
            SELECT id_user, point_spent 
            FROM ticket_registrations 
            WHERE id_event = %s AND status = 'LOSE' FOR UPDATE
        """, (id_event,))
        
        losing_tickets = cursor.fetchall()

        if not losing_tickets:
            return {
                "status": "success", 
                "message": "Tidak ada tiket berstatus LOSE yang perlu di-refund untuk event ini."
            }

        for ticket in losing_tickets:
            id_user_lose = ticket["id_user"]
            refund_amount = ticket["point_spent"]

            cursor.execute("""
                UPDATE point_balances 
                SET balance = balance + %s 
                WHERE id_user = %s
            """, (refund_amount, id_user_lose))

            cursor.execute("""
                INSERT INTO point_transactions (id_user, amount, type) 
                VALUES (%s, %s, 'refund')
            """, (id_user_lose, refund_amount))

            cursor.execute("""
                UPDATE ticket_registrations 
                SET status = 'REFUNDED' 
                WHERE id_user = %s AND id_event = %s AND status = 'LOSE'
            """, (id_user_lose, id_event))

        conn.commit()

        return {
            "status": "success",
            "message": f"Berhasil memproses refund untuk {len(losing_tickets)} pengguna yang kurang beruntung!"
        }

    except pymysql.err.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Gagal memproses refund: {str(e)}")
        
    finally:
        cursor.close()