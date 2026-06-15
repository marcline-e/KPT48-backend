from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path=".env")

# Ambil URL MySQL dari .env
DATABASE_URL = os.getenv("MYSQL_URL")

print(DATABASE_URL)
# Buat engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Base class untuk deklarasi model (Dibutuhkan untuk metadata tabel di main.py)
Base = declarative_base()

# Session database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
