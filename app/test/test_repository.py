# test_repository.py

from app.repositories.roulette_repository import (
    get_event_by_id,
    get_pending_registrants
)

print(get_event_by_id(1))

print(get_pending_registrants(1))