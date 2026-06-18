from app.core.security import get_password_hash

# Masukkan daftar 20 password yang kamu inginkan
passwords = [
    "AdminKPT48!",
    "MiskinBet123",
    "DoubleKill123",
    "MalingTiket123",
    "HappyKiyowo123",
    "UnderQuota01",
    "UnderQuota02",
    "UnderQuota03",
    "UnderQuota04",
    "UnderQuota05",
    "UnderQuota06",
    "BloodbathA1",
    "BloodbathA2",
    "BloodbathA3",
    "BloodbathA4",
    "BloodbathA5",
    "BloodbathA6",
    "BloodbathB1",
    "BloodbathB2",
    "BloodbathB3",
    "BloodbathB4",
    "BloodbathB5",
    "BloodbathB6"
]

print("Hasil Hashing Kata Sandi:\n" + "="*50)
for pwd in passwords:
    hashed = pwd_context.hash(pwd)
    print(f"Plain: {pwd}")
    print(f"Hash : {hashed}\n")