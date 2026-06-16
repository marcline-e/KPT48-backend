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