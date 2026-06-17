INSERT INTO users (email, username, full_name, nik, password_hash, role)
VALUES ('admin.theater@kpt48.com', 'admin_kpt48', 'Keputih48 Admin', '3578000000000001', '$2b$12$Ml1XV/YabR5lUSjT5aTmZOj.Z.A/HFSfjCLcvzMY0d0lD7nnBs4sS', 'ADMIN'), 
('karina@kwangya.com', 'karina_gen', 'Yoo Jimin', '3578000000000101', '$2b$12$wh.N8ZQNPr0mTGsoW/J2u.PCak3o3VT/9fn615qLlAY5u1AmTBVbu', 'GENERAL'), 
('winter@kwangya.com', 'winter_gen', 'Kim Minjeong', '3578000000000102', '$2b$12$zjCYrto8u6Xw5G248FSVX.mNz1ErmXTNninZGr73dNr3rBde7/kgq', 'GENERAL'),
('irene@rv.com', 'irene_gen', 'Bae Joohyun', '3578000000000103', '$2b$12$/pgFKElJHsxbhjiN/3QrNupn5pPTZlyQk1mTog9U3NbdnGB4muhcq', 'GENERAL'), 
('seulgi@rv.com', 'seulgi_gen', 'Kang Seulgi', '3578000000000104', '$2b$12$l0MgMIpla1mE4qx16rzDZOgYo6GGveiB4VuYHLI4hbFZLxTXDdyVq', 'GENERAL'),
('jennie@yg.com', 'jennie_gen', 'Kim Jennie', '3578000000000105', '$2b$12$JeJwa/AQatirnMYLKqFF0OxROccUs9O8aTPn.bbYUMwbvsrzbrbEO', 'GENERAL'), 
('jisoo@yg.com', 'jisoo_gen', 'Kim Jisoo', '3578000000000106', '$2b$12$sBT0fm2IrnpP9bYNhwrjXOGl4L6I3NfQ4aVieAUcdKPo6oIwhBrW.', 'GENERAL'), 
('rose@yg.com', 'rose_gen', 'Park Chaeyoung', '3578000000000107', '$2b$12$qLw8djEm57QUE1m7dxua.eo7pBmWe8aj7gH529s83yPVgByOLIB7e', 'GENERAL'),
('lisa@yg.com', 'lisa_gen', 'Lalisa Manoban', '3578000000000108', '$2b$12$tCjy6ahJ/h8Q73hLb8pCiudG.W7yde.DAAnDxLACeSNS1nyNqqL0.', 'GENERAL'),
('wonyoung@ive.com', 'wonyoung_gen', 'Jang Wonyoung', '3578000000000109', '$2b$12$pKQ7GOAjpskkFGT1GE2pieHgf6Pcw/Mq/vj09JuUMo6VUIIxFLIq6', 'GENERAL'),
('yujin@ive.com', 'yujin_gen', 'Ahn Yujin', '3578000000000110', '$2b$12$RjJeQ21BQ7b6nNLdiKbi/erVeCcYyy8NW9Jr7pShfXIYGw8AxTsE2', 'GENERAL'), 
('jin@bighit.com', 'jin_ofc', 'Kim Seokjin', '3578000000000201', '$2b$12$b8J/wLDrn38gCMzrOT/l6O3.HjZQ55cAnk4dtBzM.NboQJqXAzvGe', 'OFFICIAL'),
('suga@bighit.com', 'suga_ofc', 'Min Yoongi', '3578000000000202', '$2b$12$pDxLGFG8mH3uarEkCPSywuiQVPVK1h8huSiYVz66.q.85O6lsejfa', 'OFFICIAL'),
('jhope@bighit.com', 'jhope_ofc', 'Jung Hoseok', '3578000000000203', '$2b$12$7LNldt4ieN1Me3AW.nU.9en9MiGkynW30y7fiZFpwpWib7tMgYApC', 'OFFICIAL'),
('rm@bighit.com', 'rm_ofc', 'Kim Namjoon', '3578000000000204', '$2b$12$bPvczB//6A7Ngym6rL2lnuKNqQfPsacJU7dB3n4irzxFIqJVJn.1i', 'OFFICIAL'), 
('jimin@bighit.com', 'jimin_ofc', 'Park Jimin', '3578000000000205', '$2b$12$3NXG32KrnEFYg91Vw.2fhO9dsIopPbRwLRQzmxtwdx30ND81HZJOC', 'OFFICIAL'), 
('taehyung@bighit.com', 'v_ofc', 'Kim Taehyung', '3578000000000206', '$2b$12$AdoFDL9e4qBIy0sd8Mv4/O2mKjp.0pvxyq6wlvDTMgWN0EiXfotwi', 'OFFICIAL'),
('jungkook@bighit.com', 'jk_ofc', 'Jeon Jungkook', '3578000000000207', '$2b$12$mTYo.Nl83EfYOnRKSdOZRuqojgIRwXPVZxo8fPXOxvZBw6n6wMCly', 'OFFICIAL'),
('mingyu@svt.com', 'mingyu_ofc', 'Kim Mingyu', '3578000000000208', '$2b$12$PGfi0IwT/zz0CdGBspHFieHfGSzzgSw2xpg.Cyb2zFO2Tz2I7c3qG', 'OFFICIAL'), 
('jeonghan@svt.com', 'jeonghan_ofc', 'Yoon Jeonghan', '3578000000000209', '$2b$12$a4RorVmP9vvJJagHooJ1peSs2N5qUFSxgrp45U8lkmT1pmQoaJppW', 'OFFICIAL'),
('wonwoo@svt.com', 'wonwoo_ofc', 'Jeon Wonwoo', '3578000000000210', '$2b$12$9jrgtoNBrPF1rUL4waIhROy3s9xKKu7UnbZsizRTFp97inV9Yq1HK', 'OFFICIAL'); 

INSERT INTO point_balances (id_user, balance) VALUES
((SELECT id_user FROM users WHERE email = 'karina@kwangya.com'), 50),
((SELECT id_user FROM users WHERE email = 'winter@kwangya.com'), 120),
((SELECT id_user FROM users WHERE email = 'irene@rv.com'), 400),
((SELECT id_user FROM users WHERE email = 'seulgi@rv.com'), 0),
((SELECT id_user FROM users WHERE email = 'jennie@yg.com'), 1500),
((SELECT id_user FROM users WHERE email = 'jisoo@yg.com'), 300),
((SELECT id_user FROM users WHERE email = 'rose@yg.com'), 100),
((SELECT id_user FROM users WHERE email = 'lisa@yg.com'), 250),
((SELECT id_user FROM users WHERE email = 'wonyoung@ive.com'), 800),
((SELECT id_user FROM users WHERE email = 'yujin@ive.com'), 5),
((SELECT id_user FROM users WHERE email = 'jin@bighit.com'), 1000),
((SELECT id_user FROM users WHERE email = 'suga@bighit.com'), 500),
((SELECT id_user FROM users WHERE email = 'jhope@bighit.com'), 200),
((SELECT id_user FROM users WHERE email = 'rm@bighit.com'), 350),
((SELECT id_user FROM users WHERE email = 'jimin@bighit.com'), 75),
((SELECT id_user FROM users WHERE email = 'taehyung@bighit.com'), 600),
((SELECT id_user FROM users WHERE email = 'jungkook@bighit.com'), 2000),
((SELECT id_user FROM users WHERE email = 'mingyu@svt.com'), 150),
((SELECT id_user FROM users WHERE email = 'jeonghan@svt.com'), 0),
((SELECT id_user FROM users WHERE email = 'wonwoo@svt.com'), 450);

INSERT INTO events (set_list, event_date, total_quota, ticket_price, official_open_at, official_close_at, general_open_at, general_close_at, status) VALUES
('Pajama Drive', '2026-02-15 19:00:00', 200, 100, '2026-02-26 10:00:00', '2026-06-17 23:59:00', '2026-08-12 10:00:00', '2026-08-13 23:59:00', 'DRAFT'),
('Aturan Anti Cinta', '2026-08-20 19:00:00', 250, 150, '2026-08-15 10:00:00', '2026-08-16 23:59:00', '2026-08-17 10:00:00', '2026-08-18 23:59:00', 'DRAFT'),
('Tunas di Balik Seragam', '2026-08-25 19:00:00', 150, 120, '2026-08-20 10:00:00', '2026-08-21 23:59:00', '2026-08-22 10:00:00', '2026-08-23 23:59:00', 'DRAFT'),
('Cara Meminum Ramune', '2026-09-01 19:00:00', 300, 200, '2026-08-25 10:00:00', '2026-08-26 23:59:00', '2026-08-27 10:00:00', '2026-08-28 23:59:00', 'DRAFT'),
('Gadis-gadis Remaja', '2026-09-10 19:00:00', 200, 150, '2026-09-01 10:00:00', '2026-09-02 23:59:00', '2026-09-03 10:00:00', '2026-09-04 23:59:00', 'DRAFT');

INSERT INTO official_profiles (id_user, loss_count, is_active)
VALUES
(12, 2, 1),
(13, 1, 1),
(14, 4, 1),
(15, 3, 1),
(16, 0, 1),
(17, 5, 1),
(18, 2, 1),
(19, 1, 1),
(20, 3, 1),
(21, 0, 1);

INSERT INTO ticket_registrations
(
    id_user,
    id_event,
    phase,
    status,
    point_spent
)
VALUES
(12, 1, 'OFFICIAL', 'PENDING', 100),
(13, 1, 'OFFICIAL', 'PENDING', 100),
(14, 1, 'OFFICIAL', 'PENDING', 100),
(15, 1, 'OFFICIAL', 'PENDING', 100),
(16, 1, 'OFFICIAL', 'PENDING', 100),
(17, 1, 'OFFICIAL', 'PENDING', 100),
(18, 1, 'OFFICIAL', 'PENDING', 100),
(19, 1, 'OFFICIAL', 'PENDING', 100),
(20, 1, 'OFFICIAL', 'PENDING', 100),
(21, 1, 'OFFICIAL', 'PENDING', 100);