from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from app.database.mysql import Base

class Point_Transaction(Base):
    __tablename__ = "point_transactions"

    id_point_transaction = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    amount = Column(Integer, nullable=False) # Jumlah point yang ditransaksikan (positif untuk penambahan, negatif untuk pengurangan)
    type = Column(String(20), nullable=False) # topup, deduct, refund, membership
    reference_id = Column(Integer, ForeignKey("ticket_registrations.id_ticket_registration"), nullable=True) # Bisa diisi dengan id_ticket_registration untuk transaksi yang terkait pembelian tiket
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relasi ke tabel user (Satu Point_Transaction punya satu User)
    user = relationship("User", back_populates="point_transactions")
    tickets = relationship("TicketRegistration", back_populates="point_transaction", uselist=False)