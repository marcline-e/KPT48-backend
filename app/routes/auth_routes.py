from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import pymysql

from app.database.mysql import get_db 
from app.schemas.user_schema import UserCreate, UserResponse, UpgradeMembership
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    decode_access_token
)

# 1. Definisi Router
router = APIRouter(tags=["Authentication"])

# 2. Definisi Dependency untuk "Satpam" (Menggunakan HTTPBearer)
security_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme), 
    conn: pymysql.connections.Connection = Depends(get_db)
):
    # HTTPBearer otomatis mengambil token dari header "Authorization: Bearer <token>"
    token = credentials.credentials
    email = decode_access_token(token)
    
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    
    if not user:
        raise HTTPException(status_code=401, detail="User tidak ditemukan")
    return user

# 3. Schemas
class UserLogin(BaseModel):
    email: str
    password: str

# 4. Rute (Routes)
@router.post("/register", response_model=UserResponse)
def register_user(
    user_data: UserCreate, 
    conn: pymysql.connections.Connection = Depends(get_db)
):
    cursor = conn.cursor()
    check_query = "SELECT email FROM users WHERE email = %s"
    cursor.execute(check_query, (user_data.email,))
    db_user = cursor.fetchone()
    
    if db_user:
        cursor.close()
        raise HTTPException(status_code=400, detail="Email sudah terdaftar!")

    hashed_pwd = get_password_hash(user_data.password)
    
    insert_query = """
        INSERT INTO users (email, username, full_name, nik, password_hash)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor.execute(insert_query, (
        user_data.email,
        user_data.username,
        user_data.full_name,
        user_data.nik,
        hashed_pwd
    ))
    conn.commit()

    new_id = cursor.lastrowid
    cursor.close()
    
    return {
        "id_user": new_id,
        "email": user_data.email,
        "username": user_data.username,
        "role": "GENERAL"
    }

@router.post("/login")
def login(
    user_credentials: UserLogin, 
    conn: pymysql.connections.Connection = Depends(get_db)
):
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (user_credentials.email,))
    user = cursor.fetchone()
    cursor.close()
    
    if not user:
        raise HTTPException(status_code=404, detail="Email tidak ditemukan")

    if not verify_password(user_credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Password salah")

    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/upgrade")
def upgrade_to_official(
    payload: UpgradeMembership,
    current_user: dict = Depends(get_current_user), # Langsung dapet user dari token!
    conn: pymysql.connections.Connection = Depends(get_db)
):
    upgrade_cost = 200 # Set harga poin untuk upgrade
    id_user = current_user["id_user"] # Sesuaikan dengan nama kolom ID di database kalian
    
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    try:
        # 1. Mulai Transaksi ACID (Krusial!)
        conn.begin()

        # 2. Lock baris user dan poin biar ga ada race condition
        cursor.execute("""
            SELECT u.role, p.balance 
            FROM users u 
            JOIN point_balance p ON u.id_user = p.id_user 
            WHERE u.id_user = %s FOR UPDATE;
        """, (id_user,))
        
        user_data = cursor.fetchone()

        # 3. Validasi Bisnis
        if not user_data:
            raise HTTPException(status_code=404, detail="Data poin user tidak ditemukan.")
        if user_data['role'].upper() == 'OFFICIAL':
            raise HTTPException(status_code=400, detail="User sudah menjadi Official Member.")
        if user_data['balance'] < upgrade_cost:
            raise HTTPException(status_code=400, detail="Poin tidak mencukupi untuk upgrade.")

        # 4. Eksekusi rangkaian modifikasi data
        # Potong Poin
        cursor.execute("""
            UPDATE point_balance 
            SET balance = balance - %s, updated_at = NOW() 
            WHERE id_user = %s;
        """, (upgrade_cost, id_user))

        # Catat Log Transaksi
        cursor.execute("""
            INSERT INTO point_transaction (id_user, amount, type, created_at) 
            VALUES (%s, %s, 'membership', NOW());
        """, (id_user, upgrade_cost))

        # Update Role User
        cursor.execute("""
            UPDATE users 
            SET role = 'OFFICIAL' 
            WHERE id_user = %s;
        """, (id_user,))

        # Buat Official Profile
        cursor.execute("""
            INSERT INTO official_profile (id_user, full_name, nik, phone, is_active) 
            VALUES (%s, %s, %s, %s, 1);
        """, (id_user, payload.full_name, payload.nik, payload.phone))

        # 5. Commit transaksi jika semua mulus
        conn.commit()
        return {"status": "success", "message": "Welcome to Official Member! Poin berhasil dipotong."}

    except HTTPException:
        # Kalau errornya dari validasi kita sendiri, lempar lagi ke atas
        conn.rollback()
        raise
    except Exception as e:
        # Kalau errornya dari database, rollback dan kasih tau errornya
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database transaction failed: {str(e)}")
    finally:
        cursor.close()

@router.get("/me", dependencies=[Depends(security_scheme)])
def get_my_profile(current_user=Depends(get_current_user)):
    return {
        "email": current_user["email"],
        "username": current_user["username"],
        "full_name": current_user["full_name"],
        "role": current_user["role"]
    }