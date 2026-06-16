from fastapi import APIRouter
import pymysql
from datetime import datetime
from app.services.roulette_service import execute_roulette_service
from app.database.mysql import get_db

router = APIRouter(
    prefix="/roulette",
    tags=["Roulette"]
)

@router.post("/execute", status_code=status.HTTP_200_OK)
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