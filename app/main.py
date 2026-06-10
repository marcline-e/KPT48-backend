from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth_routes import router as auth_router
from app.routes.event_routes import router as event_router
from app.core.exception_handler import register_exception_handlers
from app.database.mysql import engine, Base
import app.models

# Ini bakal otomatis bikin tabel di kpt48_ticketing kalau tabelnya belum ada
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KPT48 Theater Ticketing API",
    description="Backend service for FP SBD 2026",
    version="1.0.0"
)

# 1. Konfigurasi CORS (Agar tidak error "Failed to fetch" di Swagger)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Registrasi Router
app.include_router(auth_router)
app.include_router(event_router)

# 3. Registrasi Global Exception Handler
register_exception_handlers(app)

@app.get("/")
async def root():
    return {"message": "Welcome to KPT48 Ticketing System! Ready for the war."}

    from fastapi import FastAPI
from app.routers import auth # Import router baru

app = FastAPI()

# Daftarkan router
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Server KPT48 Ticketing Berjalan!"}