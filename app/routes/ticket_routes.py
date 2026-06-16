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
    phase = current_user["role"]
    cursor = conn.cursor()

    if current_user["role"] == "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin tidak memiliki akses untuk membeli tiket."
        )

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
            (id_user, req.id_event, phase_terpilih, current_ticket_price) # Perhatikan phase_terpilih di sini
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

@router.post("/{id_event}/execute-roulette", status_code=status.HTTP_200_OK)
def trigger_roulette(
    id_event: int,
    phase: str, # Input dari request body/query: "OFFICIAL" atau "GENERAL"
    conn: pymysql.connections.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # 1. SECURITY CHECK: Cuma Admin yang boleh pencet tombol gacha
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Forbidden: Only admins can trigger the roulette system!"
        )

    # Pastikan pakai DictCursor agar output berupa dictionary persis seperti kodemu sebelumnya
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # 2. Ambil data penutupan event
        cursor.execute("""
            SELECT official_close_at, general_close_at 
            FROM events 
            WHERE id_event = %s
        """, (id_event,))
        event = cursor.fetchone()

        if not event:
            raise HTTPException(status_code=404, detail="Event tidak ditemukan.")

        now = datetime.now()

        # 3. TEMPORAL VALIDATION: Cegah eksekusi prematur
        if phase.upper() == "OFFICIAL":
            if now <= event["official_close_at"]:
                raise HTTPException(
                    status_code=400, 
                    detail="Hold up! Masa pendaftaran Official belum ditutup. Gacha tidak bisa dieksekusi."
                )
                
        elif phase.upper() == "GENERAL":
            if not event["general_close_at"]:
                raise HTTPException(status_code=400, detail="Jadwal General belum diatur di database.")
                
            if now <= event["general_close_at"]:
                raise HTTPException(
                    status_code=400, 
                    detail="Hold up! Masa pendaftaran General belum ditutup. Gacha tidak bisa dieksekusi."
                )
        else:
            raise HTTPException(status_code=400, detail="Fase tidak valid. Pilih OFFICIAL atau GENERAL.")

        # ================================================================
        # CHECKPOINT BERHASIL
        # Di bawah baris ini, Reyhan akan mengambil alih untuk menarik data 
        # partisipan berstatus 'PENDING' dan menjalankan komputasi roulette
        # ================================================================

        return {
            "status": "success", 
            "message": f"Validasi waktu lolos. Algoritma gacha untuk fase {phase.upper()} siap dieksekusi."
        }

    except HTTPException as he:
        # Lempar ulang error HTTP agar pesan detailnya sampai ke Postman
        raise he
        
    except pymysql.err.Error as e:
        raise HTTPException(status_code=500, detail=f"Database execution error: {str(e)}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        
    finally:
        cursor.close()