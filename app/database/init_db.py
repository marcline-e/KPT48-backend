import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    print("Memulai proses persiapan basis data...")
    
    # Buka koneksi ke MySQL
    conn = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "kpt48_ticketing")
    )
    cursor = conn.cursor()

    try:
        # 1. Mengeksekusi schema.sql
        print("Mengeksekusi schema.sql...")
        with open("app/database/schema.sql", "r") as f:
            # Pisahkan kueri berdasarkan tanda titik koma
            schema_queries = f.read().split(';')
            for query in schema_queries:
                if query.strip():
                    cursor.execute(query)
        print("Tabel berhasil dibuat!")

        # 2. Mengeksekusi seed.sql
        print("Mengeksekusi seed.sql...")
        with open("app/database/seed.sql", "r") as f:
            seed_queries = f.read().split(';')
            for query in seed_queries:
                if query.strip():
                    cursor.execute(query)
        print("Data pengujian berhasil dimasukkan!")

        conn.commit()
        print("Seluruh proses basis data selesai dengan sukses!")

    except pymysql.err.Error as e:
        print(f"Gagal mengeksekusi basis data: {e}")
        conn.rollback()
        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    setup_database()