from app.repositories.roulette_repository import (
    get_event_by_id,
    get_pending_registrants,
    update_ticket_status,
    reset_loss_count,
    increment_loss_count
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

    # update winner
    #for ticket_id in result["winner_ticket_ids"]:
        #update_ticket_status(ticket_id, "WIN")

    #for user_id in result["winner_ids"]:
        #reset_loss_count(user_id)

    # update loser
    #for ticket_id in result["loser_ticket_ids"]:
        #update_ticket_status(ticket_id, "LOSE")

    #for user_id in result["loser_ids"]:
        #increment_loss_count(user_id)

    return result