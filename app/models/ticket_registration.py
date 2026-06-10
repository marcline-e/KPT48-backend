from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database.mysql import Base

class TicketRegistration(Base):
    __tablename__ = "ticket_registrations"

    id_ticket_registration = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    # UNTUK FOREIGN KEY: Gunakan string "nama_tabel.nama_kolom"
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    id_event = Column(Integer, ForeignKey("events.id_event"), nullable=False)
    phase = Column(String(20), nullable=False) # OFFICIAL, GENERAL
    status = Column(String(20), default="PENDING") # PENDING, WIN, LOSE, REFUND_REQUESTED, REFUNDED
    point_spent = Column(Integer, nullable=False) # Berapa banyak point yang dipakai untuk beli tiket ini? 
    registered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # UNTUK RELATIONSHIP: Gunakan string "NamaClass"
    user = relationship("User", back_populates="tickets")
    event = relationship("Event", back_populates="tickets")
    point_transaction = relationship("Point_Transaction", back_populates="tickets", uselist=False)