from pydantic import BaseModel, EmailStr

# Schema ini dipakai saat user baru daftar (Register)
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    nik: str
    password: str

# Schema ini dipakai saat menampilkan data user (tanpa password agar aman!)
class UserResponse(BaseModel):
    id_user: int
    email: EmailStr
    username: str
    role: str
