from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.mysql import Base

class Official_Profile(Base):
    __tablename__ = "official_profiles"

    no_anggota = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    loss_count = Column(Integer, default=0)
    is_active = Column(Integer, default=1) # 1 untuk aktif, 0 untuk non-aktif
    last_active_at = Column(DateTime(timezone=True), nullable=True)

    # Relasi ke tabel user (Satu Official_Profile punya satu User)
    user = relationship("User", back_populates="official_profile", uselist=False)