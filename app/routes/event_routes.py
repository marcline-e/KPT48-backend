from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.mysql import get_db
from app.models.event import Event
from app.schemas.event_schema import EventCreate
from fastapi import APIRouter

router = APIRouter(
    prefix="/event",
    tags=["Event"]
)


@router.get("/test")
def event_test():
    return {
        "message": "Event route working"
    }

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

    new_event = Event(
        set_list=event.set_list,
        event_date=event.event_date,
        total_quota=event.total_quota,
        ticket_price=event.ticket_price,
        official_open_at=event.official_open_at,
        official_close_at=event.official_close_at,
        general_open_at=event.general_open_at,
        general_close_at=event.general_close_at,
        status="DRAFT"
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {
        "message": "Event berhasil dibuat",
        "id_event": new_event.id_event
    }