from app.database.mongo import mongodb
from app.database.roulette_log_schema import create_roulette_log

log = create_roulette_log(
    event_id=4,
    total_participants=26,
    total_quota=10,
    pool_a_count=17,
    pool_b_count=9,
    winner_ids=[26, 20, 9, 21, 23],
    loser_ids=[1, 2, 3, 4, 5]
)

result = mongodb["roulette_logs"].insert_one(log)

print("SUCCESS")
print("Inserted ID:", result.inserted_id)