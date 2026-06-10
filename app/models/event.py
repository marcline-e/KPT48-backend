from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.mysql import Base

class Event(Base):
    __tablename__ = "events" # Nama tabel di database nanti

    # Mendefinisikan kolom-kolom (Atribut)
    id_event = Column(Integer, primary_key=True, autoincrement=True, index=True)
    set_list = Column(String(100), nullable=False)
    event_date = Column(DateTime, nullable=False)
    total_quota = Column(Integer, nullable=False)

    # Waktu fase pendaftaran
    official_open_at = Column(DateTime, nullable=False)
    official_close_at = Column(DateTime, nullable=False)
    general_open_at = Column(DateTime, nullable=True) # Bisa True karena dibuka opsional
    general_close_at = Column(DateTime, nullable=True)
    
    status = Column(String(20), default="DRAFT") # Draft, Open, Closed

    # Relasi ke tabel tiket (Satu Event punya banyak pendaftar tiket)
    tickets = relationship("TicketRegistration", back_populates="event")