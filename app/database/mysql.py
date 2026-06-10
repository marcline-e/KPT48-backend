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
engine = create_engine(DATABASE_URL)

# Session database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class ORM
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
# Dependency database session 
def get_db():
    db = SessionLocal() 
    try: 
        yield db 
    finally: 
        db.close()