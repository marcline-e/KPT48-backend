INSERT INTO users (email, username, full_name, nik, password_hash, role)
VALUES ('admin.theater@kpt48.com', 'admin_kpt48', 'Keputih48 Admin', '3578000000000001', '$2b$12$Ml1XV/YabR5lUSjT5aTmZOj.Z.A/HFSfjCLcvzMY0d0lD7nnBs4sS', 'ADMIN'), --pw: admin123
('karina@kwangya.com', 'karina_gen', 'Yoo Jimin', '3578000000000101', '$2b$12$wh.N8ZQNPr0mTGsoW/J2u.PCak3o3VT/9fn615qLlAY5u1AmTBVbu', 'GENERAL'), --karina123
('winter@kwangya.com', 'winter_gen', 'Kim Minjeong', '3578000000000102', '$2b$12$zjCYrto8u6Xw5G248FSVX.mNz1ErmXTNninZGr73dNr3rBde7/kgq', 'GENERAL'), --winter123
('irene@rv.com', 'irene_gen', 'Bae Joohyun', '3578000000000103', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'GENERAL'),
('seulgi@rv.com', 'seulgi_gen', 'Kang Seulgi', '3578000000000104', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'GENERAL'),
('jennie@yg.com', 'jennie_gen', 'Kim Jennie', '3578000000000105', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'GENERAL'),
('jisoo@yg.com', 'jisoo_gen', 'Kim Jisoo', '3578000000000106', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'GENERAL'),
('rose@yg.com', 'rose_gen', 'Park Chaeyoung', '3578000000000107', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'GENERAL'),
('lisa@yg.com', 'lisa_gen', 'Lalisa Manoban', '3578000000000108', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'GENERAL'),
('wonyoung@ive.com', 'wonyoung_gen', 'Jang Wonyoung', '3578000000000109', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'GENERAL'),
('yujin@ive.com', 'yujin_gen', 'Ahn Yujin', '3578000000000110', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'GENERAL'),
('jin@bighit.com', 'jin_ofc', 'Kim Seokjin', '3578000000000201', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'OFFICIAL'),
('suga@bighit.com', 'suga_ofc', 'Min Yoongi', '3578000000000202', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'OFFICIAL'),
('jhope@bighit.com', 'jhope_ofc', 'Jung Hoseok', '3578000000000203', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'OFFICIAL'),
('rm@bighit.com', 'rm_ofc', 'Kim Namjoon', '3578000000000204', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'OFFICIAL'),
('jimin@bighit.com', 'jimin_ofc', 'Park Jimin', '3578000000000205', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'OFFICIAL'),
('taehyung@bighit.com', 'v_ofc', 'Kim Taehyung', '3578000000000206', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'OFFICIAL'),
('jungkook@bighit.com', 'jk_ofc', 'Jeon Jungkook', '3578000000000207', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'OFFICIAL'),
('mingyu@svt.com', 'mingyu_ofc', 'Kim Mingyu', '3578000000000208', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'OFFICIAL'),
('jeonghan@svt.com', 'jeonghan_ofc', 'Yoon Jeonghan', '3578000000000209', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'OFFICIAL'),
('wonwoo@svt.com', 'wonwoo_ofc', 'Jeon Wonwoo', '3578000000000210', '$2b$12$EixZaYVK1fsby1Z7KSt6O.V5a67mP4eS/85X2wO2r1lTETXm2V9aW', 'OFFICIAL');

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



