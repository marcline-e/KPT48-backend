from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.point_balance import PointBalance
from app.models.point_transaction import PointTransaction
from app.models.ticket_registration import TicketRegistration
from app.models.event import Event

def register_ticket_service(
    db: Session,
    user_id: int,
    event_id: int
):

    try:
        # CEK EVENT
        event = db.query(Event).filter(
            Event.id == event_id
        ).first()

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event tidak ditemukan"
            )

        
        # CEK POINT BALANCE
        
        balance = db.query(PointBalance).filter(
            PointBalance.user_id == user_id
        ).first()

        if not balance:
            raise HTTPException(
                status_code=404,
                detail="Point balance tidak ditemukan"
            )

        
        # CEK SALDO
        
        if balance.balance < event.ticket_price:
            raise HTTPException(
                status_code=400,
                detail="Saldo tidak cukup"
            )

        
        # KURANGI SALDO
       
        balance.balance -= event.ticket_price

       
        # CATAT POINT TRANSACTION
        
        point_transaction = PointTransaction(
            user_id=user_id,
            amount=event.ticket_price,
            transaction_type="deduct"
        )

        db.add(point_transaction)

        
        # BUAT TICKET REGISTRATION
        
        ticket = TicketRegistration(
            user_id=user_id,
            event_id=event_id,
            status="PENDING",
            point_spent=event.ticket_price
        )

        db.add(ticket)

        
        # COMMIT TRANSACTION
        
        raise Exception("TEST ROLLBACK")

        db.commit()

        # Refresh object
        db.refresh(ticket)

        return {
            "success": True,
            "message": "Pendaftaran tiket berhasil",
            "ticket_id": ticket.id,
            "status": ticket.status
        }

    except Exception as e:
        # rollback otomatis
        db.rollback()
        raise e

