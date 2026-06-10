from datetime import datetime


def create_roulette_log(
    event_id,
    total_participants,
    total_quota,
    pool_a_count,
    pool_b_count,
    winner_ids,
    loser_ids
):
    return {
        "event_id": event_id,
        "executed_at": datetime.utcnow(),

        "total_participants": total_participants,
        "total_quota": total_quota,

        "pool_a_count": pool_a_count,
        "pool_b_count": pool_b_count,

        "winner_ids": winner_ids,
        "loser_ids": loser_ids
    }