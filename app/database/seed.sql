INSERT INTO users (email, username, full_name, nik, password_hash, role)
VALUES (
    'admin.theater@kpt48.com', 
    'admin_kpt48', 
    'Keputih48 Admin', 
    '3578000000000001', 
    -- Catatan: password_hash ini adalah hasil enkripsi dari kata 'admin123' menggunakan bcrypt
    '$2b$12$Ml1XV/YabR5lUSjT5aTmZOj.Z.A/HFSfjCLcvzMY0d0lD7nnBs4sS', 
    'ADMIN'
);

INSERT INTO events (
    set_list,
    event_date,
    total_quota,
    ticket_price,
    official_open_at,
    official_close_at,
    general_open_at,
    general_close_at,
    status
)
VALUES (
    'Summer Festival',
    '2025-12-01 19:00:00',
    10,
    100000,
    '2025-11-01 00:00:00',
    '2025-11-05 23:59:59',
    '2025-11-06 00:00:00',
    '2025-11-10 23:59:59',
    'OPEN'
);

INSERT INTO users (
    email,
    username,
    full_name,
    nik,
    password_hash,
    role
)
VALUES
('andi@test.com','andi','Andi','1111','test','GENERAL'),
('budi@test.com','budi','Budi','2222','test','GENERAL'),
('citra@test.com','citra','Citra','3333','test','GENERAL'),
('eko@test.com','eko','Eko','4444','test','GENERAL');

INSERT INTO official_profiles (
    id_user,
    loss_count,
    is_active
)
VALUES
(2,2,1),
(3,1,1),
(4,4,1),
(5,3,1);

INSERT INTO ticket_registrations (
    id_user,
    id_event,
    phase,
    status,
    point_spent
)
VALUES
(2,1,'OFFICIAL','PENDING',0),
(3,1,'OFFICIAL','PENDING',0),
(4,1,'OFFICIAL','PENDING',0),
(5,1,'OFFICIAL','PENDING',0);