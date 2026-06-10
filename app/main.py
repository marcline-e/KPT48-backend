from fastapi import FastAPI
from app.database.mysql import Base, engine
from app.models import User, Event, TicketRegistration  

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KPT48 Theater Ticketing API",
    description="Backend service for FP SBD 2026",
    version="1.0.0"
)

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