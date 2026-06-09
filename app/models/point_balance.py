from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from app.database.mysql import Base

class Point_Balance(Base):
    __tablename__ = "point_balances"

    id_point_balance = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    balance = Column(Integer, default=0)
    last_updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relasi ke tabel user (Satu Point_Balance punya satu User)
    user = relationship("User", back_populates="point_balance", uselist=False)