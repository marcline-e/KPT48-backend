from fastapi import APIRouter

router = APIRouter(
    prefix="/event",
    tags=["Event"]
)


@router.get("/test")
def event_test():
    return {
        "message": "Event route working"
    }

