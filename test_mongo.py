from app.repositories.roulette_log_repository import (
    save_roulette_log
)

test_data = {
    "event_id": 1,
    "message": "MongoDB test"
}

result = save_roulette_log(test_data)

print("Inserted ID:", result)