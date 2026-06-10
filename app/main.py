from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth_routes import router as auth_router
from app.routes.event_routes import router as event_router
from app.core.exception_handler import register_exception_handlers
from app.database.mysql import engine, Base
import app.models

# 1. Inisialisasi Database (Membuat tabel jika belum ada)
# Tips: Di aplikasi besar, ini biasanya ditaruh di dalam 'lifespan' event, 
# tapi untuk proyek ini, cara ini sudah sangat oke.
Base.metadata.create_all(bind=engine)

# 2. Inisialisasi Aplikasi
app = FastAPI(
    title="KPT48 Theater Ticketing API",
    description="Backend service for FP SBD 2026",
    version="1.0.0"
)

# 3. Middleware CORS (Penting untuk koneksi ke Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Registrasi Global Exception Handler
# Pastikan fungsi ini tidak menabrak middleware
register_exception_handlers(app)

# 5. Registrasi Router
# Urutan ini sudah benar, FastAPI akan membaca endpoint dari file routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(event_router, prefix="/event", tags=["Event"])

@app.get("/")
async def root():
    return {"message": "Welcome to KPT48 Ticketing System! Ready for the war."}