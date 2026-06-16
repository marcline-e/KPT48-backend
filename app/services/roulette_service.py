from app.repositories.roulette_repository import (
    get_event_by_id,
    get_pending_registrants,
    batch_update_ticket_status,
    batch_reset_loss_count,
    batch_increment_loss_count
)

from app.repositories.roulette_log_repository import (
    save_roulette_log
)

from app.services.roulette_algorithm import execute_roulette


def execute_roulette_service(event_id):

    event = get_event_by_id(event_id)

    if not event:
        raise Exception("Event tidak ditemukan")

    if event["status"] != "OPEN":
        raise Exception("Event belum dibuka")

    participants = get_pending_registrants(event_id)

    if not participants:
        raise Exception("Tidak ada peserta pending")

    result = execute_roulette(
        participants=participants,
        total_quota=event["quota"],
        id_event=event_id
    )

    # ==========================
    # DAY 7 - ROULETTE LOG
    # ==========================
    log_document = {
        "event_id": result["id_event"],
        "total_participants": result["total_participants"],
        "total_quota": result["total_quota"],

        "pool_a_count": result["pool_a_count"],
        "pool_b_count": result["pool_b_count"],

        "winner_count": len(result["winner_ids"]),
        "loser_count": len(result["loser_ids"]),

        "winner_ids": result["winner_ids"],
        "loser_ids": result["loser_ids"]
    }

    save_roulette_log(log_document)


    return result