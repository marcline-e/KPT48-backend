import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    # Fungsi ini akan dipanggil setiap kali API membutuhkan akses ke database
    connection = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""), 
        database=os.getenv("DB_NAME", "kpt48_ticketing"),
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def get_db():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()