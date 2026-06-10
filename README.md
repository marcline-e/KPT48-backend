# KPT48 Theater Ticketing API (Fondasi)

Proyek ini adalah boilerplate/fondasi untuk sistem ticketing teater KPT48 menggunakan FastAPI. Proyek ini mendukung koneksi ke dua jenis database: MySQL (SQLAlchemy) dan MongoDB (PyMongo).

## Struktur Proyek

```text
KPT48-fondasi/
├── app/
│   ├── core/
│   │   └── exception_handler.py  # Handler error global
│   ├── database/
│   │   ├── mongo.py              # Konfigurasi MongoDB
│   │   └── mysql.py              # Konfigurasi MySQL
│   ├── routes/
│   │   ├── auth_routes.py        # Endpoint Autentikasi
│   │   └── event_routes.py       # Endpoint Event
│   └── main.py                   # Entry point aplikasi
├── .env                          # Konfigurasi variabel lingkungan
├── test_mongo.py                 # Script uji coba MongoDB
└── test_mysql.py                 # Script uji coba MySQL
```

## Persiapan

1. **Virtual Environment**:
   Pastikan Anda menggunakan virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/macOS
   deactivate # untuk keluar
   # atau
   .\venv\Scripts\activate   # Untuk Windows
   ```

2. **Instalasi Dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Konfigurasi Environment**:
   Salin `.env.example` menjadi `.env` dan sesuaikan nilainya:
   ```bash
   cp .env.example .env
   ```

## Cara Menjalankan

Jalankan server pengembangan menggunakan Uvicorn:
```bash
uvicorn app.main:app --reload
```
API akan tersedia di `http://127.0.0.1:8000`.

## Dokumentasi API

Setelah server berjalan, akses dokumentasi interaktif di:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`