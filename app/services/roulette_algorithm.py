import random

TOTAL_QUOTA = 6
K = 0.15


# ======================================
# POOLING
# ======================================

def split_pool(participants):

    pool_a = []
    pool_b = []

    for user in participants:

        if user["loss_count"] > 0:
            pool_a.append(user)
        else:
            pool_b.append(user)

    return pool_a, pool_b


# ======================================
# QUOTA
# ======================================

def calculate_quota(total_quota):

    ta = int(total_quota * 0.7)
    tb = total_quota - ta

    return ta, tb


def apply_spillover(pool_a, pool_b, ta, tb):

    if len(pool_a) < ta:

        spill = ta - len(pool_a)

        tb += spill
        ta = len(pool_a)

    elif len(pool_b) < tb:

        spill = tb - len(pool_b)

        ta += spill
        tb = len(pool_b)

    return ta, tb


# ======================================
# WEIGHT
# ======================================

def calculate_weight(loss_count):

    return 1 + (loss_count * K)


def add_weight(participants):

    for user in participants:
        user["weight"] = calculate_weight(user["loss_count"])


# ======================================
# ROULETTE
# ======================================

def select_winner(pool):

    total_weight = sum(user["weight"] for user in pool)

    random_number = random.uniform(0, total_weight)

    cumulative_weight = 0

    for user in pool:

        cumulative_weight += user["weight"]

        if random_number <= cumulative_weight:
            return user


def draw_winners(pool, quota):

    winners = []

    working_pool = pool.copy()

    for _ in range(min(quota, len(working_pool))):

        winner = select_winner(working_pool)

        winners.append(winner)

        working_pool.remove(winner)

    return winners


# ======================================
# MAIN SERVICE
# ======================================

def execute_roulette(participants, total_quota, id_event):

    add_weight(participants)

    print("\nPARTICIPANTS")

    for p in participants:
        print(p)

    pool_a, pool_b = split_pool(participants)

    ta, tb = calculate_quota(total_quota)

    ta, tb = apply_spillover(
        pool_a,
        pool_b,
        ta,
        tb
    )

    pool_a_winners = draw_winners(pool_a, ta)

    pool_b_winners = draw_winners(pool_b, tb)

    all_winners = pool_a_winners + pool_b_winners

    winner_user_ids = [
        user["user_id"]
        for user in all_winners
    ]

    winner_ticket_ids = [
        user["ticket_id"]
        for user in all_winners
    ]

    losers = []

    for user in participants:

        if user["user_id"] not in winner_user_ids:
            losers.append(user)

    loser_user_ids = [
        user["user_id"]
        for user in losers
    ]

    loser_ticket_ids = [
        user["ticket_id"]
        for user in losers
    ]

    return {
        "id_event":id_event,
        "total_participants": len(participants),
        "total_quota": total_quota,

        "pool_a_count": len(pool_a),
        "pool_b_count": len(pool_b),

        "winner_ids": winner_user_ids,
        "winner_ticket_ids": winner_ticket_ids,

        "loser_ids": loser_user_ids,
        "loser_ticket_ids": loser_ticket_ids
    }


# ======================================
# TEST
# ======================================

if __name__ == "__main__":

    result = execute_roulette(
        participants=participants,
        total_quota=TOTAL_QUOTA,
        id_event=1
    )

    print("\n=== ROULETTE RESULT ===")

    for key, value in result.items():
        print(f"{key}: {value}")