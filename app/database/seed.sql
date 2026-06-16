INSERT INTO users (email, username, full_name, nik, password_hash, role)
VALUES (
    'admin.theater@kpt48.com', 
    'admin_kpt48', 
    'Keputih48 Admin', 
    '3578000000000001', 
    -- Catatan: password_hash ini adalah hasil enkripsi dari kata 'admin123' menggunakan bcrypt
    '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 
    'ADMIN'
);
