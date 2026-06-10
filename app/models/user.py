from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship
from app.database.mysql import Base

class User(Base):
    __tablename__ = "users" # Ini nama tabel di MySQL

    id_user = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String(100), nullable=False, unique=True)
    username = Column(String(50), nullable=False)
    full_name = Column(String(100), nullable=False)
    nik = Column(String(20), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="GENERAL")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # MAGIC HAPPENS HERE: 
    # Tulis "TicketRegistration" pakai tanda kutip, jangan di-import class-nya!
    tickets = relationship("TicketRegistration", back_populates="user")
    official_profile = relationship("Official_Profile", back_populates="user", uselist=False)
    point_balance = relationship("Point_Balance", back_populates="user", uselist=False)
    point_transactions = relationship("Point_Transaction", back_populates="user")