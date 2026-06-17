from fastapi import APIRouter, Depends, HTTPException, status
import pymysql

from app.database.mysql import get_db
from app.schemas.event_schema import EventCreate, EventUpdate
from app.routes.auth_routes import get_current_user

router = APIRouter(
    tags=["Event"]
)


# @router.get("/test")
# def event_test():
#     return {
#         "message": "Event route working"
#     }

@router.post("/event")
def create_event(
    event: EventCreate,
    conn: pymysql.connections.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    # KUNCI EXCEPTION ROLE ADMIN
    if current_user["role"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akses ditolak! Anda bukan Administrator."
        )
    
    if event.total_quota <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quota harus lebih dari 0"
        )

    if event.official_open_at >= event.official_close_at:
        raise HTTPException(
            status_code=400,
            detail="Official phase tidak valid"
        )

    if event.general_open_at >= event.general_close_at:
        raise HTTPException(
            status_code=400,
            detail="General phase tidak valid"
        )

    cursor = conn.cursor()
    insert_query = """
        INSERT INTO events (set_list, event_date, total_quota, ticket_price, 
                          official_open_at, official_close_at, general_open_at, 
                          general_close_at, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'DRAFT')
    """

    try:
        # Eksekusi dengan parameter tuple untuk mencegah SQL Injection
        cursor.execute(insert_query, (
            event.set_list, 
            event.event_date, 
            event.total_quota, 
            event.ticket_price, 
            event.official_open_at, 
            event.official_close_at, 
            event.general_open_at, 
            event.general_close_at
        ))
        conn.commit() # Wajib commit!
        new_event_id = cursor.lastrowid

    except pymysql.err.Error as e:
        conn.rollback() # Kalau gagal insert, batalkan transaksi
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    finally:
        cursor.close()

    return {
        "message": "Event berhasil dibuat oleh admin",
        "id_event": new_event_id
    }

@router.put("/{event_id}/update")
def update_event(
    event_id: int,
    event: EventUpdate,
    conn: pymysql.connections.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Akses ditolak! Khusus Admin.")

    cursor = conn.cursor()
    
    # Cek apakah event ada
    cursor.execute("SELECT id_event FROM events WHERE id_event = %s", (event_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Event tidak ditemukan")

    update_query = """
        UPDATE events 
        SET set_list = %s, event_date = %s, total_quota = %s, ticket_price = %s,
            official_open_at = %s, official_close_at = %s, general_open_at = %s, general_close_at = %s
        WHERE id_event = %s
    """
    
    try:
        cursor.execute(update_query, (
            event.set_list, event.event_date, event.total_quota, event.ticket_price,
            event.official_open_at, event.official_close_at, event.general_open_at, event.general_close_at,
            event_id
        ))
        conn.commit()
    except pymysql.err.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()

    return {"message": f"Event {event_id} berhasil di-update!"}

@router.delete("/{event_id}/delete")
def delete_event(
    event_id: int,
    conn: pymysql.connections.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Akses ditolak! Khusus Admin.")

    cursor = conn.cursor()
    
    try:
        # Hapus event (MySQL akan otomatis menghapus tiket yang terkait jika ON DELETE CASCADE aktif)
        cursor.execute("DELETE FROM events WHERE id_event = %s", (event_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Event tidak ditemukan")
        conn.commit()
    except pymysql.err.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()

    return {"message": f"Event {event_id} berhasil dihapus beserta data tiketnya!"}