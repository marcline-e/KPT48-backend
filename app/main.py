from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth_routes import router as auth_router
from app.routes.event_routes import router as event_router
from app.routes.ticket_routes import router as ticket_routes
from app.core.exception_handler import register_exception_handlers
from app.routes.transaction_routes import router as transaction_router
from app.routes.roulette_routes import router as roulette_router


# SEMUA IMPORT APP.MODELS SUDAH DIHAPUS DI SINI

app = FastAPI(
    title="KPT48 Theater Ticketing API",
    version="1.0.0"
)

# --- Middleware & Router ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrasi Global Exception Handler
register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(event_router)
app.include_router(ticket_routes)
app.include_router(transaction_router)
app.include_router(roulette_router)

@app.get("/")
async def root():
    return {"message": "Welcome to KPT48 Ticketing System!"}