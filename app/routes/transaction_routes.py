from fastapi import APIRouter, Depends, HTTPException, status
import pymysql

from app.database.mysql import get_db
from app.schemas.transaction_schema import TopUpRequest
from app.routes.auth_routes import get_current_user 

router = APIRouter(tags=["Transaction"])

@router.post("/topup")
def topup_points(
    request: TopUpRequest, 
    conn: pymysql.connections.Connection = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["id_user"]
    cursor = conn.cursor()
    
    try:
        # 1. Mulai Transaksi (ACID Compliance)
        conn.begin()

        # 2. Cek saldo saat ini dan KUNCI BARIS (FOR UPDATE)
        balance_query = "SELECT balance FROM point_balances WHERE id_user = %s FOR UPDATE"
        cursor.execute(balance_query, (user_id,))
        wallet = cursor.fetchone()
        
        if not wallet:
            # Insert dompet baru jika user belum pernah punya record saldo
            insert_wallet = "INSERT INTO point_balances (id_user, balance) VALUES (%s, 0)"
            cursor.execute(insert_wallet, (user_id,))
            current_balance = 0
        else:
            current_balance = wallet["balance"]
        
        new_balance = current_balance + request.amount
        
        # 3. Update saldo
        update_query = "UPDATE point_balances SET balance = %s WHERE id_user = %s"
        cursor.execute(update_query, (new_balance, user_id))
        
        # 4. Catat riwayat transaksi
        history_query = """
            INSERT INTO point_transactions (id_user, amount, type) 
            VALUES (%s, %s, 'topup')
        """
        cursor.execute(history_query, (user_id, request.amount))
        
        # 5. Simpan semua perubahan secara permanen
        conn.commit()
        
        return {
            "success": True,
            "message": f"Berhasil top-up {request.amount} poin!",
            "current_balance": new_balance
        }

    except pymysql.err.Error as e:
        # Jika database error, batalkan semua eksekusi!
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Gagal memproses top up: {str(e)}")
        
    finally:
        # Tutup cursor untuk menghemat memori server
        cursor.close()