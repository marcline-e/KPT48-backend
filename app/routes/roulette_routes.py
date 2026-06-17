from fastapi import APIRouter, Depends, HTTPException, status, Query
import pymysql
from datetime import datetime
from app.services.roulette_service import execute_roulette_service
from app.database.mysql import get_db
from app.routes.auth_routes import get_current_user

router = APIRouter(
    tags=["Roulette"]
)

@router.post("/{id_event}/execute", status_code=status.HTTP_200_OK)
def trigger_roulette(
    id_event: int,
    phase: str = Query(..., description="Fase eksekusi: OFFICIAL atau GENERAL"),
    current_user: dict = Depends(get_current_user)
):
    
    if current_user.get("role") != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Akses ditolak! Hanya Admin yang dapat mengeksekusi roulette."
        )

    phase = phase.upper()
    if phase not in ["OFFICIAL", "GENERAL"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parameter phase tidak valid. Gunakan 'OFFICIAL' atau 'GENERAL'."
        )    

    try:
        result = execute_roulette_service(id_event)

        return {
            "success": True,
            "message": "Roulette executed successfully",
            "data": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )