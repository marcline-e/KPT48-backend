from pydantic import BaseModel, Field

class TopUpRequest(BaseModel):
    # Field(..., gt=0) artinya wajib diisi dan angkanya harus lebih besar dari 0
    amount: int = Field(..., gt=0, description="Jumlah poin yang ingin di-topup")