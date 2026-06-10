import random

participants = [
    {"id": 1, "name": "Andi", "loss_count": 0},
    {"id": 2, "name": "Budi", "loss_count": 2},
    {"id": 3, "name": "Citra", "loss_count": 1},
    {"id": 4, "name": "Dina", "loss_count": 0},
    {"id": 5, "name": "Eko", "loss_count": 4},
    {"id": 6, "name": "Farah", "loss_count": 3},
    {"id": 7, "name": "Gilang", "loss_count": 0},
    {"id": 8, "name": "Hana", "loss_count": 2},
    {"id": 9, "name": "Indra", "loss_count": 5},
    {"id": 10, "name": "Jihan", "loss_count": 1},
    {"id": 11, "name": "Kevin", "loss_count": 0},
    {"id": 12, "name": "Lala", "loss_count": 3},
    {"id": 13, "name": "Miko", "loss_count": 0},
    {"id": 14, "name": "Nadia", "loss_count": 4},
    {"id": 15, "name": "Oka", "loss_count": 2},
    {"id": 16, "name": "Putri", "loss_count": 0},
    {"id": 17, "name": "Qori", "loss_count": 1},
    {"id": 18, "name": "Rizky", "loss_count": 6},
    {"id": 19, "name": "Salsa", "loss_count": 0},
    {"id": 20, "name": "Teguh", "loss_count": 3},
    {"id": 21, "name": "Umar", "loss_count": 2},
    {"id": 22, "name": "Vina", "loss_count": 0},
    {"id": 23, "name": "Wahyu", "loss_count": 5},
    {"id": 24, "name": "Xena", "loss_count": 1},
    {"id": 25, "name": "Yusuf", "loss_count": 0},
    {"id": 26, "name": "Zahra", "loss_count": 4},
]

# Membagi peserta menjadi Pool A dan Pool B.
# Pool A berisi peserta yang pernah kalah sebelumnya.
def split_pool(participants):

    pool_a = []
    pool_b = []

    for user in participants:
        if user["loss_count"] > 0:
            pool_a.append(user)
        else:
            pool_b.append(user)

    return pool_a, pool_b

pool_a, pool_b = split_pool(participants)


# Menghitung pembagian kuota awal.
# Pool A mendapat 70%, Pool B mendapat 30%.
def calculate_quota(total_quota):

    ta = int(total_quota * 0.7)
    tb = total_quota - ta

    return ta, tb


# Spillover digunakan ketika salah satu pool
# tidak memiliki peserta yang cukup untuk memenuhi kuota.
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

total_quota = 10

ta, tb = calculate_quota(total_quota)

ta, tb = apply_spillover(
    pool_a,
    pool_b,
    ta,
    tb
)

# Menghitung bonus peluang berdasarkan jumlah kekalahan sebelumnya.
K = 0.15

def calculate_weight(loss_count):

    return 1 + (loss_count * K)

for user in participants:
    user["weight"] = calculate_weight(user["loss_count"])


# Weighted random selection.
# Peserta dengan weight lebih besar memiliki peluang lebih tinggi.
def select_winner(pool):

    total_weight = sum(user["weight"] for user in pool)
    random_number = random.uniform(0, total_weight)

    cumulative_weight = 0

    for user in pool:

        cumulative_weight += user["weight"]

        if random_number <= cumulative_weight:
            return user


# Memilih pemenang sesuai kuota dan
# mencegah peserta menang lebih dari satu kali.
def draw_winners(pool, quota):

    winners = []
    working_pool = pool.copy()

    for _ in range(min(quota, len(working_pool))):

        winner = select_winner(working_pool)

        winners.append(winner)
        working_pool.remove(winner)

    return winners

pool_a_winners = draw_winners(pool_a, ta)
pool_b_winners = draw_winners(pool_b, tb)

print("\nPOOL A WINNERS")
for user in pool_a_winners:
    print(user)

print("\nPOOL B WINNERS")
for user in pool_b_winners:
    print(user)

all_winners = pool_a_winners + pool_b_winners


# Menentukan peserta yang kalah.
# Data ini nantinya digunakan untuk update loss_count
# dan proses refund point.
winner_ids = {user["id"] for user in all_winners}

losers = []

for user in participants:
    if user["id"] not in winner_ids:
        losers.append(user)

print("\nLOSERS")
for user in losers:
    print(user)


# Simulasi statistik digunakan untuk membuktikan
# bahwa weight mempengaruhi peluang kemenangan.
def simulate_statistics():

    results = {}

    for user in participants:
        results[user["name"]] = 0

    for _ in range(50000):

        winner = select_winner(participants)

        results[winner["name"]] += 1

    return results

stats = simulate_statistics()

print("\n=== STATISTICS ===")

for name, count in sorted(
    stats.items(),
    key=lambda x: x[1],
    reverse=True
):
    print(name, count)