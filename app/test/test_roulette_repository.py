from app.repositories.roulette_repository import *

print("=== EVENT ===")
print(get_event_by_id(1))

print("\n=== PENDING ===")
print(get_pending_registrants(1))

print("\n=== RESET LOSS ===")
reset_loss_count(1)
print("OK")

print("\n=== INCREMENT LOSS ===")
increment_loss_count(1)
print("OK")

print("\n=== UPDATE STATUS ===")
update_ticket_status(1, "WIN")
print("OK")