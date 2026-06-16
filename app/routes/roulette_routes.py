from fastapi import APIRouter
from app.services.roulette_service import execute_roulette_service

router = APIRouter(
    prefix="/roulette",
    tags=["Roulette"]
)

@router.post("/event/{event_id}/execute")
def execute_roulette(event_id: int):

    result = execute_roulette_service(event_id)

    return result