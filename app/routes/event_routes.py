from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.mysql import get_db
from app.schemas.event_schema import EventCreate

router = APIRouter(
    prefix="/event",
    tags=["Event"]
)


# @router.get("/test")
# def event_test():
#     return {
#         "message": "Event route working"
#     }

@router.post("/")
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    
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

    insert_query = text("""
        INSERT INTO events (set_list, event_date, total_quota, ticket_price, 
                          official_open_at, official_close_at, general_open_at, 
                          general_close_at, status)
        VALUES (:set_list, :event_date, :total_quota, :ticket_price, 
                :official_open_at, :official_close_at, :general_open_at, 
                :general_close_at, 'DRAFT')
    """)
    
    result = db.execute(insert_query, {
        "set_list": event.set_list,
        "event_date": event.event_date,
        "total_quota": event.total_quota,
        "ticket_price": event.ticket_price,
        "official_open_at": event.official_open_at,
        "official_close_at": event.official_close_at,
        "general_open_at": event.general_open_at,
        "general_close_at": event.general_close_at
    })
    db.commit()

    return {
        "message": "Event berhasil dibuat",
        "id_event": result.lastrowid
    }