-- Hapus tabel lama jika ada agar tidak bentrok saat di-run ulang
-- Urutan DROP harus dari tabel anak (yang punya Foreign Key) ke tabel induk
DROP TABLE IF EXISTS point_transactions;
DROP TABLE IF EXISTS ticket_registrations;
DROP TABLE IF EXISTS point_balances;
DROP TABLE IF EXISTS official_profiles;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS users;

-- 1. Tabel users
CREATE TABLE users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    nik VARCHAR(20) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'GENERAL',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Tabel events
CREATE TABLE events (
    id_event INT AUTO_INCREMENT PRIMARY KEY,
    set_list VARCHAR(100) NOT NULL,
    event_date DATETIME NOT NULL,
    total_quota INT NOT NULL,
    ticket_price INT NOT NULL,
    official_open_at DATETIME NOT NULL,
    official_close_at DATETIME NOT NULL,
    general_open_at DATETIME NULL,
    general_close_at DATETIME NULL,
    status VARCHAR(20) DEFAULT 'DRAFT'
);

-- 3. Tabel official_profiles
CREATE TABLE official_profiles (
    no_anggota INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    loss_count INT DEFAULT 0,
    is_active INT DEFAULT 1,
    last_active_at TIMESTAMP NULL,
    CONSTRAINT fk_official_user FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE
);

-- 4. Tabel point_balances
CREATE TABLE point_balances (
    id_point_balance INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    balance INT DEFAULT 0,
    last_updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_balance_user FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE
);

-- 5. Tabel ticket_registrations
CREATE TABLE ticket_registrations (
    id_ticket_registration INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    id_event INT NOT NULL,
    phase VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    point_spent INT NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ticket_user FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE,
    CONSTRAINT fk_ticket_event FOREIGN KEY (id_event) REFERENCES events(id_event) ON DELETE CASCADE
);

-- 6. Tabel point_transactions
CREATE TABLE point_transactions (
    id_point_transaction INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    amount INT NOT NULL,
    type VARCHAR(20) NOT NULL,
    reference_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_transaction_user FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE,
    CONSTRAINT fk_transaction_ticket FOREIGN KEY (reference_id) REFERENCES ticket_registrations(id_ticket_registration) ON DELETE SET NULL
);