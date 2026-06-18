# 🎭 KPT48 Theater Ticketing System

> **Final Project — Sistem Basis Data 2026**
> Kelompok 4 | Teknik Informatika ITS

| NRP | Nama | Peran |
|-----|------|-------|
| 5027251017 | Viko Rizky Fauzan | Data Architect & Infrastructure |
| 5027251031 | Dian Piramidiana Rachmatika | Auth & Account Manager |
| 5027251044 | Arrumanta Ekna Luhkinasih | Core Transaction Engineer |
| 5027251080 | Reyhan Adi Satrio | Algorithm & Logic Master |

---

## Daftar Isi

1. [Pendahuluan](#1-pendahuluan)
2. [Fungsionalitas Sistem](#2-fungsionalitas-sistem)
3. [Desain Database](#3-desain-database)
4. [Implementasi Database Lanjutan](#4-implementasi-database-lanjutan)
5. [Arsitektur Backend](#5-arsitektur-backend)
6. [Kesimpulan](#6-kesimpulan)

---

## 1. Pendahuluan

### 1.1 Latar Belakang

KPT48 (Keputih48) merupakan sister idol group fiktif dari JKT48 yang berada di bawah naungan 48 Produce. Sebagaimana idol group pada umumnya, KPT48 secara rutin menyelenggarakan pertunjukan teater yang disebut **KPT48 Theater** sebagai sarana interaksi langsung antara member dan penggemar.

Untuk dapat menghadiri pertunjukan tersebut, penggemar harus melakukan pendaftaran melalui website resmi KPT48. Mengingat kapasitas teater yang terbatas serta tingginya minat penggemar, diperlukan sebuah sistem ticketing yang mampu mengelola proses pendaftaran, seleksi pemenang tiket, pembayaran, hingga pengembalian dana (refund) secara terstruktur dan efisien.

### 1.2 Identifikasi Masalah

Berdasarkan proses ticketing KPT48 Theater, terdapat beberapa permasalahan utama:

1. **Kuota Theater Terbatas** — Jumlah pendaftar sering kali melebihi jumlah tiket yang tersedia, sehingga diperlukan mekanisme seleksi yang adil.

2. **Probabilitas Roulette** — Sistem roulette tidak bersifat sepenuhnya acak. Pengguna yang pernah kalah pada periode sebelumnya perlu mendapat prioritas lebih tinggi agar distribusi kesempatan lebih merata.

3. **Pengelolaan Dua Fase Ticketing** — Sistem menerapkan dua fase pembelian (Official dan General) dengan waktu dan hak akses yang berbeda, sehingga diperlukan mekanisme penjadwalan yang presisi.

4. **Keseimbangan Kesempatan Official vs. General Member** — Official Member mendapat akses lebih awal, namun sistem harus tetap memberikan kesempatan kepada General Member agar tidak menghambat pertumbuhan fanbase baru.

### 1.3 Tujuan Sistem

**Tujuan Umum:** Membangun sistem ticketing KPT48 Theater yang mampu mengelola proses pendaftaran tiket, pelaksanaan roulette, pengelolaan poin, serta proses refund secara terstruktur, adil, dan efisien melalui pemanfaatan basis data relasional (MySQL) dan non-relasional (MongoDB).

**Tujuan Khusus:**
- Mengelola data pengguna berdasarkan tiga jenis keanggotaan: Admin, Official Member, dan General Member.
- Mengimplementasikan sistem ticketing dua fase sesuai aturan dan hak akses masing-masing keanggotaan.
- Mengimplementasikan mekanisme roulette dengan probabilitas dinamis berdasarkan riwayat kekalahan.
- Mengelola sistem poin sebagai alat transaksi, termasuk pemotongan poin dan refund otomatis.
- Mengelola status tiket menggunakan mekanisme state machine: `PENDING → WIN / LOSE → REFUNDED`.
- Menyimpan log hasil eksekusi roulette ke MongoDB untuk keperluan audit dan analitik.

---

## 2. Fungsionalitas Sistem

### 2.1 Fitur Utama

#### 👤 Manajemen Akun
| Fitur | Deskripsi |
|-------|-----------|
| Register & Login | Pembuatan akun dengan hashing password (bcrypt) dan autentikasi JWT |
| Role-Based Access | Tiga role: `ADMIN`, `OFFICIAL`, `GENERAL` — masing-masing memiliki hak akses berbeda |
| Upgrade Membership | General Member dapat upgrade ke Official dengan memotong 200 poin |
| Update & Delete Profil | Pengguna dapat memperbarui atau menghapus akunnya sendiri |

#### 🎪 Manajemen Event (Khusus Admin)
| Fitur | Deskripsi |
|-------|-----------|
| CRUD Event | Membuat, mengubah, menghapus event pertunjukan |
| Toggle Status | Mengubah status event: `DRAFT → OPEN → CLOSED` |
| Pengaturan Fase | Set jadwal buka/tutup untuk fase Official dan General secara independen |

#### 🎫 Sistem Ticketing
| Fitur | Deskripsi |
|-------|-----------|
| Fase Official | Hanya Official Member yang bisa mendaftar pada rentang waktu official |
| Fase General | Hanya General Member yang bisa mendaftar setelah fase Official berakhir |
| Transaksi ACID | Pendaftaran tiket dilindungi dengan database transaction + row-level locking (`FOR UPDATE`) |
| Cek Status Tiket | Pengguna dapat melihat seluruh riwayat registrasi tiket miliknya |

#### 💰 Sistem Poin
| Fitur | Deskripsi |
|-------|-----------|
| Top-Up Poin | Pengguna dapat mengisi saldo poin kapan saja |
| Cek Saldo | Endpoint untuk melihat saldo poin saat ini |
| Pemotongan Otomatis | Poin terpotong saat mendaftar tiket, tercatat di `point_transactions` |
| Refund Otomatis | Admin memproses refund poin bagi peserta yang kalah roulette |

#### 🎰 Sistem Roulette / Gacha (Khusus Admin)
| Fitur | Deskripsi |
|-------|-----------|
| Pooling Peserta | Peserta dibagi ke Pool A (pernah kalah, `loss_count > 0`) dan Pool B (belum pernah kalah) |
| Kuota Dinamis | Pool A mendapat 70% kuota, Pool B mendapat 30% kuota |
| Mekanisme Spillover | Sisa kuota pool yang kekurangan peserta dialihkan ke pool lainnya |
| Probabilitas Berbobot | Bobot setiap peserta dihitung dengan formula `W_i = 1 + (loss_count × K)` di mana K = 0.15 |
| Batch State Update | Status tiket diperbarui secara massal (WIN/LOSE) setelah undian selesai |
| Log ke MongoDB | Seluruh parameter dan hasil roulette dicatat ke koleksi `roulette_logs` di MongoDB |

### 2.2 Alasan Pemisahan Database

Sistem ini menggunakan **dua jenis database** untuk kebutuhan yang berbeda:

| | MySQL (Relasional) | MongoDB (Non-Relasional) |
|--|---|---|
| **Digunakan untuk** | Data transaksional: users, events, tickets, poin | Log hasil roulette |
| **Alasan** | Data memiliki relasi kompleks dan membutuhkan ACID compliance (transaksi tiket tidak boleh partial — harus berhasil semua atau rollback semua) | Data log bersifat analitik, tidak ada relasi, strukturnya fleksibel, dan lebih cepat di-query sebagai dokumen utuh |
| **Contoh query kritis** | JOIN users → tickets → points dalam satu transaksi atomik | `find({ event_id: X })` untuk melihat histori roulette suatu event |

---

## 3. Desain Database

### 3.1 Identifikasi Entitas

Sistem ini memiliki **6 entitas utama** pada MySQL dan **1 koleksi** pada MongoDB:

#### `users`
Menyimpan data akun seluruh pengguna sistem.
- `id_user` (PK), `email` (UNIQUE), `username`, `full_name`, `nik` (UNIQUE), `password_hash`, `role` (`ADMIN`/`OFFICIAL`/`GENERAL`), `created_at`, `updated_at`

#### `official_profiles`
Menyimpan data tambahan khusus untuk Official Member.
- `no_anggota` (PK, AUTO_INCREMENT), `id_user` (FK → users), `loss_count`, `is_active`, `last_active_at`

#### `point_balances`
Menyimpan total saldo poin setiap pengguna.
- `id_point_balance` (PK), `id_user` (FK → users), `balance`, `last_updated_at`

#### `point_transactions`
Menyimpan seluruh riwayat perubahan poin (audit trail).
- `id_point_transaction` (PK), `id_user` (FK → users), `amount`, `type` (`topup`/`deduct`/`refund`/`membership`), `reference_id` (FK → ticket_registrations, nullable), `created_at`

#### `events`
Menyimpan data pertunjukan teater.
- `id_event` (PK), `set_list` (UNIQUE), `event_date`, `total_quota`, `ticket_price`, `official_open_at`, `official_close_at`, `general_open_at`, `general_close_at`, `status` (`DRAFT`/`OPEN`/`CLOSED`)

#### `ticket_registrations`
Menyimpan data pendaftaran tiket per pengguna per event.
- `id_ticket_registration` (PK), `id_user` (FK → users), `id_event` (FK → events), `phase` (`OFFICIAL`/`GENERAL`), `status` (`PENDING`/`WIN`/`LOSE`/`REFUNDED`), `point_spent`, `registered_at`

#### Koleksi MongoDB: `roulette_logs`
Menyimpan log hasil eksekusi roulette untuk keperluan audit dan analitik.
```json
{
  "event_id": 1,
  "phase": "OFFICIAL",
  "executed_at": "2026-06-17T10:00:00Z",
  "total_participants": 10,
  "total_quota": 6,
  "pool_a_count": 6,
  "pool_b_count": 4,
  "winner_ids": [12, 14, 17, 13, 16, 18],
  "loser_ids": [15, 19, 20, 21]
}
```
> Menggunakan **embedding** (bukan referencing) karena seluruh data log disimpan dan dibaca sebagai satu kesatuan dokumen — tidak ada kebutuhan JOIN ke koleksi lain.

### 3.2 Relasi Antar Entitas

```
users (1) ──────── (0..1) official_profiles     [Hanya role OFFICIAL]
users (1) ──────── (1)    point_balances         [Setiap user punya tepat 1 saldo]
users (1) ──────── (N)    point_transactions     [Riwayat transaksi poin]
users (1) ──────── (N)    ticket_registrations   [Bisa daftar ke banyak event]
events (1) ─────── (N)    ticket_registrations   [Satu event, banyak pendaftar]
ticket_registrations (1) ─ (N) point_transactions [Satu tiket bisa memicu >1 transaksi: deduct + refund]
events (1) ─────── (N)    roulette_logs (MongoDB) [Satu event bisa punya 2 log: Official & General]
```

### 3.3 Desain Tabel MySQL

```sql
-- Tabel users
CREATE TABLE users (
    id_user       INT AUTO_INCREMENT PRIMARY KEY,
    email         VARCHAR(100) NOT NULL UNIQUE,
    username      VARCHAR(50) NOT NULL,
    full_name     VARCHAR(100) NOT NULL,
    nik           VARCHAR(20) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role          VARCHAR(20) DEFAULT 'GENERAL',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP
);

-- Tabel events
CREATE TABLE events (
    id_event          INT AUTO_INCREMENT PRIMARY KEY,
    set_list          VARCHAR(100) NOT NULL UNIQUE,
    event_date        DATETIME NOT NULL,
    total_quota       INT NOT NULL,
    ticket_price      INT NOT NULL,
    official_open_at  DATETIME NOT NULL,
    official_close_at DATETIME NOT NULL,
    general_open_at   DATETIME NULL,
    general_close_at  DATETIME NULL,
    status            VARCHAR(20) DEFAULT 'DRAFT'
);

-- Tabel official_profiles
CREATE TABLE official_profiles (
    no_anggota    INT AUTO_INCREMENT PRIMARY KEY,
    id_user       INT NOT NULL,
    loss_count    INT DEFAULT 0,
    is_active     INT DEFAULT 1,
    last_active_at TIMESTAMP NULL,
    CONSTRAINT fk_official_user FOREIGN KEY (id_user)
        REFERENCES users(id_user) ON DELETE CASCADE
);

-- Tabel point_balances
CREATE TABLE point_balances (
    id_point_balance INT AUTO_INCREMENT PRIMARY KEY,
    id_user          INT NOT NULL,
    balance          INT DEFAULT 0,
    last_updated_at  TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_balance_user FOREIGN KEY (id_user)
        REFERENCES users(id_user) ON DELETE CASCADE
);

-- Tabel ticket_registrations
CREATE TABLE ticket_registrations (
    id_ticket_registration INT AUTO_INCREMENT PRIMARY KEY,
    id_user    INT NOT NULL,
    id_event   INT NOT NULL,
    phase      VARCHAR(20) NOT NULL,
    status     VARCHAR(20) DEFAULT 'PENDING',
    point_spent INT NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ticket_user  FOREIGN KEY (id_user)  REFERENCES users(id_user)   ON DELETE CASCADE,
    CONSTRAINT fk_ticket_event FOREIGN KEY (id_event) REFERENCES events(id_event) ON DELETE CASCADE
);

-- Tabel point_transactions
CREATE TABLE point_transactions (
    id_point_transaction INT AUTO_INCREMENT PRIMARY KEY,
    id_user      INT NOT NULL,
    amount       INT NOT NULL,
    type         VARCHAR(20) NOT NULL,
    reference_id INT NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_transaction_user   FOREIGN KEY (id_user)      REFERENCES users(id_user)                              ON DELETE CASCADE,
    CONSTRAINT fk_transaction_ticket FOREIGN KEY (reference_id) REFERENCES ticket_registrations(id_ticket_registration) ON DELETE SET NULL
);
```

### 3.4 Desain Koleksi MongoDB

**Database:** `kpt48_logs` | **Koleksi:** `roulette_logs`

| Field | Tipe | Keterangan |
|-------|------|-----------|
| `event_id` | Integer | ID event yang diroulette (referensi ke MySQL) |
| `phase` | String | `"OFFICIAL"` atau `"GENERAL"` |
| `executed_at` | DateTime | Waktu eksekusi roulette (UTC) |
| `total_participants` | Integer | Total peserta PENDING |
| `total_quota` | Integer | Total kuota tiket yang diperebutkan |
| `pool_a_count` | Integer | Jumlah peserta di Pool A (loss_count > 0) |
| `pool_b_count` | Integer | Jumlah peserta di Pool B (loss_count = 0) |
| `winner_ids` | Array[Int] | List user ID pemenang |
| `loser_ids` | Array[Int] | List user ID yang kalah |

**Keputusan desain:** Menggunakan **embedding penuh** (semua data dalam satu dokumen) karena:
- Log roulette selalu dibaca secara utuh, tidak pernah diakses per-field secara terpisah.
- Tidak ada koleksi lain di MongoDB yang perlu dirujuk.
- Struktur flat dan konsisten, sehingga tidak memerlukan `$lookup` (JOIN) antar koleksi.

---

## 4. Implementasi Database Lanjutan

### 4.1 Stored Procedure / Service Layer

Alih-alih stored procedure di level database, logika kompleks diimplementasikan sebagai **Python service layer** yang mengeksekusi serangkaian query secara atomik menggunakan `conn.begin()` dan `conn.commit() / conn.rollback()`.

#### Proses Pendaftaran Tiket (Atomic Transaction)
Setiap pendaftaran tiket menjalankan 3 operasi dalam satu transaksi:
```
1. SELECT ... FOR UPDATE  → Kunci baris event & saldo poin (mencegah race condition)
2. UPDATE point_balances  → Potong saldo pengguna
3. INSERT ticket_registrations → Buat tiket dengan status PENDING
4. INSERT point_transactions   → Catat log pemotongan poin (type: 'deduct')
```
Jika salah satu langkah gagal → `conn.rollback()` membatalkan semua perubahan.

#### Proses Upgrade Membership (Atomic Transaction)
```
1. SELECT ... FOR UPDATE  → Kunci data user & saldo
2. Validasi role & saldo  → Tolak jika sudah Official atau saldo < 200
3. UPDATE point_balances  → Potong 200 poin
4. INSERT point_transactions → Catat transaksi (type: 'membership')
5. UPDATE users           → Ubah role menjadi 'OFFICIAL'
6. INSERT official_profiles  → Buat profil Official baru
```

#### Proses Refund (Batch Transaction)
```
1. SELECT tiket LOSE untuk event tertentu   → Ambil semua yang kalah
2. Untuk setiap tiket kalah:
   a. UPDATE point_balances  → Kembalikan poin
   b. INSERT point_transactions → Catat refund (type: 'refund')
   c. UPDATE ticket_registrations → Ubah status ke 'REFUNDED'
3. COMMIT jika semua sukses
```

### 4.2 Batch Update (Pengganti Trigger)

Setelah roulette selesai, sistem melakukan **batch update** secara efisien menggunakan `IN` clause:

```python
# Batch update status tiket pemenang
UPDATE ticket_registrations
SET status = 'WIN'
WHERE id_ticket_registration IN (id1, id2, id3, ...)

# Batch reset loss_count untuk pemenang Official
UPDATE official_profiles
SET loss_count = 0
WHERE id_user IN (user1, user2, ...)

# Batch tambah loss_count untuk yang kalah Official
UPDATE official_profiles
SET loss_count = loss_count + 1
WHERE id_user IN (user_x, user_y, ...)
```

### 4.3 Query View (Implicit)

Query untuk mendapatkan data peserta roulette menggunakan JOIN yang berfungsi layaknya sebuah view:

```sql
SELECT
    tr.id_ticket_registration,
    u.id_user,
    u.username,
    COALESCE(op.loss_count, 0) AS loss_count
FROM ticket_registrations tr
JOIN users u ON tr.id_user = u.id_user
LEFT JOIN official_profiles op ON u.id_user = op.id_user
WHERE
    tr.id_event = %s
    AND tr.status = 'PENDING'
    AND tr.phase = %s;
```
> `LEFT JOIN` digunakan agar General Member (yang tidak memiliki `official_profiles`) tetap bisa ikut roulette General dengan `loss_count = 0` (via `COALESCE`).

### 4.4 Row-Level Locking (FOR UPDATE)

Untuk mencegah race condition pada operasi concurrent (banyak user mendaftar sekaligus), sistem menggunakan `SELECT ... FOR UPDATE` yang mengunci baris hingga transaksi selesai:

```sql
-- Kunci saldo poin user agar tidak bisa diubah proses lain
SELECT balance FROM point_balances WHERE id_user = %s FOR UPDATE;

-- Kunci data event agar kuota tidak berubah di tengah proses
SELECT * FROM events WHERE id_event = %s FOR UPDATE;
```

---

## 5. Arsitektur Backend

### 5.1 Teknologi yang Digunakan

| Komponen | Teknologi | Versi |
|----------|-----------|-------|
| Framework | FastAPI | Latest |
| Database Relasional | MySQL | 8.x |
| Database Non-Relasional | MongoDB | Latest |
| Driver MySQL | PyMySQL | Latest |
| Driver MongoDB | PyMongo | Latest |
| Autentikasi | JWT (python-jose) | HS256 |
| Password Hashing | bcrypt | Latest |
| Validasi Schema | Pydantic | v2 |
| Env Management | python-dotenv | Latest |

### 5.2 Struktur Proyek

```
KPT48-backend/
├── app/
│   ├── main.py                    # Entry point FastAPI, registrasi router & middleware
│   ├── core/
│   │   ├── security.py            # JWT, bcrypt hashing/verification
│   │   └── exception_handler.py   # Global exception handler
│   ├── database/
│   │   ├── mysql.py               # Koneksi & dependency injection MySQL
│   │   ├── mongo.py               # Koneksi MongoDB
│   │   ├── schema.sql             # DDL tabel MySQL
│   │   ├── seed.sql               # Data awal untuk pengujian
│   │   ├── init_db.py             # Script inisialisasi database
│   │   └── roulette_log_schema.py # Builder dokumen MongoDB
│   ├── routes/
│   │   ├── auth_routes.py         # Register, Login, Upgrade, Profil
│   │   ├── event_routes.py        # CRUD Event & Toggle Status
│   │   ├── ticket_routes.py       # Daftar Tiket, Cek Status, Refund
│   │   ├── transaction_routes.py  # Top-Up & Cek Saldo Poin
│   │   └── roulette_routes.py     # Eksekusi Roulette
│   ├── schemas/
│   │   ├── user_schema.py         # Pydantic schema untuk User
│   │   ├── event_schema.py        # Pydantic schema untuk Event
│   │   ├── ticket_schema.py       # Pydantic schema untuk Tiket
│   │   └── transaction_schema.py  # Pydantic schema untuk Transaksi
│   ├── services/
│   │   ├── roulette_algorithm.py  # Logika gacha: pooling, bobot, undian
│   │   └── roulette_service.py    # Orkestrasi eksekusi roulette + log MongoDB
│   └── repositories/
│       ├── roulette_repository.py      # Query MySQL khusus roulette
│       └── roulette_log_repository.py  # Operasi tulis ke MongoDB
├── .env.example                   # Contoh konfigurasi environment
└── README.md
```

### 5.3 API Endpoint

#### 🔐 Authentication (`/`)
| Method | Endpoint | Role | Deskripsi |
|--------|----------|------|-----------|
| `POST` | `/register` | Public | Daftar akun baru (role: GENERAL) |
| `POST` | `/login` | Public | Login, mendapatkan JWT token |
| `POST` | `/upgrade` | GENERAL | Upgrade ke Official Member (potong 200 poin) |
| `GET` | `/me` | All | Lihat profil sendiri |
| `PUT` | `/me/update` | All | Perbarui data profil |
| `DELETE` | `/me/delete` | All | Hapus akun secara permanen |

#### 🎪 Event Management (`/event`)
| Method | Endpoint | Role | Deskripsi |
|--------|----------|------|-----------|
| `POST` | `/event` | ADMIN | Buat event baru |
| `PUT` | `/{event_id}/update` | ADMIN | Perbarui data event |
| `PATCH` | `/{event_id}/status` | ADMIN | Ubah status event (DRAFT/OPEN/CLOSED) |
| `DELETE` | `/{event_id}/delete` | ADMIN | Hapus event |

#### 🎫 Ticketing (`/tickets`)
| Method | Endpoint | Role | Deskripsi |
|--------|----------|------|-----------|
| `POST` | `/tickets` | OFFICIAL/GENERAL | Daftar tiket (otomatis deteksi fase) |
| `GET` | `/status` | All | Lihat semua tiket milik sendiri |
| `POST` | `/{id_event}/refund` | ADMIN | Proses refund massal peserta LOSE |

#### 💰 Transaksi Poin (`/`)
| Method | Endpoint | Role | Deskripsi |
|--------|----------|------|-----------|
| `POST` | `/topup` | All | Isi saldo poin |
| `GET` | `/balance` | All | Cek saldo poin saat ini |

#### 🎰 Roulette (`/`)
| Method | Endpoint | Role | Deskripsi |
|--------|----------|------|-----------|
| `POST` | `/{id_event}/execute?phase=OFFICIAL\|GENERAL` | ADMIN | Eksekusi undian roulette |

### 5.4 Fitur Unggulan

#### Algoritma Roulette Berbobot
Ini adalah inti sistem. Setiap peserta mendapatkan bobot probabilitas berdasarkan riwayat kekalahannya:

```python
K = 0.15  # Konstanta bobot

def calculate_weight(loss_count):
    return 1 + (loss_count * K)
    # loss_count=0 → bobot 1.00 (probabilitas dasar)
    # loss_count=2 → bobot 1.30 (30% lebih mungkin menang)
    # loss_count=5 → bobot 1.75 (75% lebih mungkin menang)

def select_winner(pool):
    total_weight = sum(user["weight"] for user in pool)
    random_number = random.uniform(0, total_weight)
    cumulative = 0
    for user in pool:
        cumulative += user["weight"]
        if random_number <= cumulative:
            return user  # Pemenang terpilih
```

#### Mekanisme Spillover
Saat salah satu pool kekurangan peserta, sisa kuotanya dialihkan:
```python
def apply_spillover(pool_a, pool_b, ta, tb):
    if len(pool_a) < ta:          # Pool A kekurangan peserta
        spill = ta - len(pool_a)
        tb += spill               # Sisa kuota dialihkan ke Pool B
        ta = len(pool_a)
    elif len(pool_b) < tb:        # Pool B kekurangan peserta
        spill = tb - len(pool_b)
        ta += spill               # Sisa kuota dialihkan ke Pool A
        tb = len(pool_b)
    return ta, tb
```

#### JWT Authentication Middleware
Setiap endpoint yang membutuhkan autentikasi menggunakan dependency injection FastAPI:
```python
def get_current_user(credentials = Depends(HTTPBearer()), conn = Depends(get_db)):
    token = credentials.credentials
    email = decode_access_token(token)  # Verifikasi JWT
    # Query user dari database berdasarkan email dari token
    ...
    return user
```

---

## 6. Kesimpulan

Proyek **KPT48 Theater Ticketing System** berhasil mengimplementasikan sistem basis data hybrid yang menggabungkan MySQL untuk data transaksional dan MongoDB untuk data log analitik. Beberapa pencapaian utama:

1. **ACID Compliance** — Seluruh operasi kritis (pendaftaran tiket, upgrade membership, refund) dieksekusi dalam transaksi atomik dengan row-level locking untuk mencegah race condition.

2. **Algoritma Roulette Adil** — Sistem probabilitas berbobot memastikan peserta dengan riwayat kekalahan lebih banyak mendapat kesempatan lebih besar, menciptakan distribusi tiket yang lebih merata dari waktu ke waktu.

3. **Arsitektur Bersih** — Pemisahan yang jelas antara routes (controller), services (business logic), dan repositories (data access layer) membuat kode mudah dipelihara dan diuji.

4. **Keamanan** — Password di-hash menggunakan bcrypt, autentikasi menggunakan JWT HS256, dan seluruh query menggunakan parameterized query untuk mencegah SQL injection.

5. **Skalabilitas Log** — Penggunaan MongoDB untuk log roulette memungkinkan penyimpanan data analitik yang fleksibel tanpa membebani skema relasional MySQL.

---

*Final Project Sistem Basis Data 2026 — Institut Teknologi Sepuluh Nopember*
