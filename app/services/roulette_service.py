from datetime import datetime

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
from app.database.roulette_log_schema import create_roulette_log



def execute_roulette_service(event_id, phase):

    event = get_event_by_id(event_id)

    if not event:
        raise Exception("Event tidak ditemukan")

    if event["status"] != "OPEN":
        raise Exception("Event belum dibuka")

    now = datetime.now()
    if phase == "OFFICIAL":
        if now <= event["official_close_at"]:
            raise Exception(f"Fase Official belum ditutup. Eksekusi ditolak hingga {event['official_close_at']}")
    elif phase == "GENERAL":
        if event["general_close_at"] is None or now <= event["general_close_at"]:
            raise Exception("Fase General belum ditutup atau jadwal belum diset oleh Admin.")

    participants = get_pending_registrants(event_id, phase)

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
    log_document = create_roulette_log(
        event_id=result["id_event"],
        total_participants=result["total_participants"],
        total_quota=result["total_quota"],
        pool_a_count=result["pool_a_count"],
        pool_b_count=result["pool_b_count"],
        winner_ids=result["winner_ids"],
        loser_ids=result["loser_ids"]
    )
    log_document["phase"] = phase 
    save_roulette_log(log_document)

    if result["winner_ticket_ids"]:
        batch_update_ticket_status(result["winner_ticket_ids"], "WIN")
        # Khusus Official, loss count di-reset agar adil di war selanjutnya
        if phase == "OFFICIAL":
            batch_reset_loss_count(result["winner_ids"])
    
    if result["loser_ticket_ids"]:
        batch_update_ticket_status(result["loser_ticket_ids"], "LOSE")
        # Khusus Official, loss count ditambah untuk prioritas gacha selanjutnya
        if phase == "OFFICIAL":
            batch_increment_loss_count(result["loser_ids"])

    return result