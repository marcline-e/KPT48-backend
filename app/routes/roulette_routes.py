from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
import pymysql
from datetime import datetime
from app.services.roulette_service import execute_roulette_service
from app.database.mysql import get_db
from app.routes.auth_routes import get_current_user

router = APIRouter(
    prefix="/roulette",
    tags=["Roulette"]
)

@router.post("/{id_event}/execute", status_code=status.HTTP_200_OK)
def trigger_roulette(
    id_event: int,
    current_user: dict = Depends(get_current_user)
):
    
    if current_user.get("role") != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Only admin can execute roulette"
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