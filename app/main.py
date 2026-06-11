from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth_routes import router as auth_router
from app.routes.event_routes import router as event_router
from app.core.exception_handler import register_exception_handlers
from app.database.mysql import engine, Base

Base.metadata.create_all(bind=engine)

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

register_exception_handlers(app)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(event_router, prefix="/event", tags=["Event"])

@app.get("/")
async def root():
    return {"message": "Welcome to KPT48 Ticketing System!"}