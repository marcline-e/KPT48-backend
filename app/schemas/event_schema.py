from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    set_list: str
    event_date: datetime

    total_quota: int
    ticket_price: int

    official_open_at: datetime
    official_close_at: datetime

    general_open_at: datetime
    general_close_at: datetime