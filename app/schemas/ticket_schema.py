from pydantic import BaseModel

class TicketRegisterSchema(BaseModel):
    id_event: int
    phase: str  # Wajib diisi "OFFICIAL" atau "GENERAL" [cite: 383]