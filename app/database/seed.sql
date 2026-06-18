-- =========================================================================
-- KPT48 THEATER TICKETING SYSTEM - NEW SCHEMA SEED DATA FOR QA TESTING
-- =========================================================================

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE point_transactions;
TRUNCATE TABLE ticket_registrations;
TRUNCATE TABLE point_balances;
TRUNCATE TABLE official_profiles;
TRUNCATE TABLE events;
TRUNCATE TABLE users;

SET FOREIGN_KEY_CHECKS = 1;

-- =========================================================================
-- 1. INSERT USERS
-- =========================================================================
INSERT INTO users (id_user, email, username, full_name, nik, password_hash, role, created_at) VALUES
-- User Manajemen
(1, 'admin@kpt48.com', 'Admin JOT', 'Administrator Pusat', '3570000000000001', '$2b$12$TPBVKR3QfmdJol6bPLUEAOMsnPrbXngAy3Z//SKZJKy4NUiLhw0JS', 'ADMIN', NOW()),

-- User untuk API Test Pendaftaran (TC1 - TC4)
(2, 'miskin@kpt48.com', 'Official Miskin', 'Member Miskin', '3570000000000002', '$2b$12$ne7nLB8Q7nHSOgzneavvK.3CPMieZBMspxbotnyiBNlTjhURiuL2O', 'OFFICIAL', NOW()),
(3, 'double@kpt48.com', 'Official Double', 'Member Double', '3570000000000003', '$2b$12$MEeSLzdojiUBBNAPlwcdguNgqRmDoMDGwsWnFMGr639AVB7FR5Hx2', 'OFFICIAL', NOW()),
(4, 'general@kpt48.com', 'General Maling', 'Member Maling', '3570000000000004', '$2b$12$NBnIelCxjgHT8puQa9Jrmu1FZE/pMbNqEyb4QWWOkHcDH.S1QDZXq', 'GENERAL', NOW()),
(5, 'happy@kpt48.com', 'Official Happy', 'Member Happy', '3570000000000005', '$2b$12$hVNk2nptQkm9idJ/6p.sk.5LK2hNlQv3RhmJrQyBXxLDoQAdgyEBC', 'OFFICIAL', NOW()),

-- User untuk Test Gacha Under Quota (Event 2)
(10, 'u1@kpt48.com', 'Under 1', 'Peserta Under 1', '3570000000000010', '$2b$12$KoRlNlhKtwpGARyennP5h.nk/xtbiI9WxdRwVCEjyzV5AxeTcPBgK', 'OFFICIAL', NOW()),
(11, 'u2@kpt48.com', 'Under 2', 'Peserta Under 2', '3570000000000011', '$2b$12$gW4Wjah8TFkEFJNgPkhRHORN0sRL.AXTAPjsGMg2KinfyIFbgoxIe', 'OFFICIAL', NOW()),
(12, 'u3@kpt48.com', 'Under 3', 'Peserta Under 3', '3570000000000012', '$2b$12$Di2kEnU/hEUa7gRzg012AuWtT2gYMQQH4B3j5HrGhrAlohVObj/ma', 'OFFICIAL', NOW()),
(13, 'u4@kpt48.com', 'Under 4', 'Peserta Under 4', '3570000000000013', '$2b$12$ksKfBmMcBnkMsz7xx88iyOPKFtmZAfj3BrSUh1ryVoEtivBisIJEq', 'OFFICIAL', NOW()),
(14, 'u5@kpt48.com', 'Under 5', 'Peserta Under 5', '3570000000000014', '2b$12$4Zk50hUEA15a8wwGj7GeuOFK1TA.I50/Q4VI17JjvPKkhwzdsSuqy', 'OFFICIAL', NOW()),
(15, 'u6@kpt48.com', 'Under 6', 'Peserta Under 6', '3570000000000015', '$2b$12$Ur0TvrPjJbnRjeWbYBGNaOVqtMIo6u9.IPSrvwCuDasEOH1ZvcJDS', 'OFFICIAL', NOW()),

-- User untuk Test Gacha Over Quota / Bloodbath (Event 3) - Pool A (Punya kekalahan)
(20, 'oa1@kpt48.com', 'Over A1', 'Peserta Over A1', '3570000000000020', '$2b$12$NKX0MyIpF9XZ0jy2VjnUq.2oHfI.Jy0nJvRQWt3gygtkRNgEoWQ.a', 'OFFICIAL', NOW()),
(21, 'oa2@kpt48.com', 'Over A2', 'Peserta Over A2', '3570000000000021', '$2b$12$qNeZ4IYefPVrmDkVrJ8MxuZ8g0UlRCJwX8aStYCDvg69/ZkDgF5Wa', 'OFFICIAL', NOW()),
(22, 'oa3@kpt48.com', 'Over A3', 'Peserta Over A3', '3570000000000022', '$2b$12$l3ssF8C28Z4DNjG0Yba3euIgSBpTboqBA9y8i.UxXMOcc/ISQ..u6', 'OFFICIAL', NOW()),
(23, 'oa4@kpt48.com', 'Over A4', 'Peserta Over A4', '3570000000000023', '$2b$12$VjOlJZLlqWPMtu5HGttipOuCW6Xb7YsVyYRBWbLChaQxyDsn1Wbhu', 'OFFICIAL', NOW()),
(24, 'oa5@kpt48.com', 'Over A5', 'Peserta Over A5', '3570000000000024', '$2b$12$wOaL.9P.8/x7pxqNQpByYucosmAXUzOAPvFeG2ylYnwFdijJDjYSa', 'OFFICIAL', NOW()),
(25, 'oa6@kpt48.com', 'Over A6', 'Peserta Over A6', '3570000000000025', '$2b$12$bGSUy1eHz6b1bEaX4k1brOKgOTwY/IZoqJnJcDz6iI67/ZPL6/H8K', 'OFFICIAL', NOW()),

-- User untuk Test Gacha Over Quota / Bloodbath (Event 3) - Pool B (Belum pernah kalah)
(26, 'ob1@kpt48.com', 'Over B1', 'Peserta Over B1', '3570000000000026', '$2b$12$K/jvApiNXx9Fl/M8cfH4neG5QX1JfjwLYJ58NejhGo2auPiyg3r8.', 'OFFICIAL', NOW()),
(27, 'ob2@kpt48.com', 'Over B2', 'Peserta Over B2', '3570000000000027', '$2b$12$3Ux3UTINm.3Xwk4DYamXF.BzTSxtllCZWeHgD1gYtyCFH9cQGkhGy', 'OFFICIAL', NOW()),
(28, 'ob3@kpt48.com', 'Over B3', 'Peserta Over B3', '3570000000000028', '$2b$12$19fR2AsY/5OTVm13KBulx.wJP/quuD4S5tirUqT67GKU.aZT00EoW', 'OFFICIAL', NOW()),
(29, 'ob4@kpt48.com', 'Over B4', 'Peserta Over B4', '3570000000000029', '$2b$12$/W4JQiVQUQSO2R50jyu3leLMGRh9CNcK/gG5TzQC7Mi.bgXbc/mC.', 'OFFICIAL', NOW()),
(30, 'ob5@kpt48.com', 'Over B5', 'Peserta Over B5', '3570000000000030', '$2b$12$L2na1qYCvogmOu3t3cSHveI5U39igl6Jn0swV3vRw2lBa3Qd4eKG2', 'OFFICIAL', NOW()),
(31, 'ob6@kpt48.com', 'Over B6', 'Peserta Over B6', '3570000000000031', '$2b$12$Omopai.giHXHQgBDWIosCernppFwo0SwUaffkKbO60ih29KqBlUDO', 'OFFICIAL', NOW());

-- =========================================================================
-- 2. INSERT OFFICIAL PROFILES
-- Sesuai schema baru, akumulasi loss_count dipindahkan ke sini
-- =========================================================================
INSERT INTO official_profiles (id_user, loss_count, is_active) VALUES
(2, 0, 1), (3, 0, 1), (5, 0, 1), 
(10, 0, 1), (11, 0, 1), (12, 0, 1), (13, 0, 1), (14, 0, 1), (15, 0, 1),
-- Inject Loss Count khusus Pool A (Event Over Quota)
(20, 2, 1), (21, 1, 1), (22, 4, 1), (23, 2, 1), (24, 1, 1), (25, 3, 1),
-- Inject Loss Count khusus Pool B (Event Over Quota)
(26, 0, 1), (27, 0, 1), (28, 0, 1), (29, 0, 1), (30, 0, 1), (31, 0, 1);

-- =========================================================================
-- 3. INSERT POINT BALANCES
-- =========================================================================
INSERT INTO point_balances (id_user, balance) VALUES
(1, 0),        -- Admin
(2, 0),        -- TC1: Saldo 0
(3, 1000),     -- TC2
(4, 1000),     -- TC3 (General)
(5, 1000);     -- TC4
-- Inject untuk sisa user gacha
INSERT INTO point_balances (id_user, balance)
SELECT id_user, 1000 FROM users WHERE id_user >= 10;

-- =========================================================================
-- 4. INSERT EVENTS
-- =========================================================================
INSERT INTO events (id_event, set_list, event_date, total_quota, ticket_price, official_open_at, official_close_at, general_open_at, general_close_at, status) VALUES
-- EVENT 1: Fase Official SEDANG BERLANGSUNG
(1, 'Pajama Drive', NOW() + INTERVAL 5 DAY, 100, 100, NOW() - INTERVAL 1 DAY, NOW() + INTERVAL 1 DAY, NOW() + INTERVAL 2 DAY, NOW() + INTERVAL 3 DAY, 'OPEN'),

-- EVENT 2: Fase Official SUDAH TUTUP, Kuota 10 (Under Quota)
(2, 'Aturan Anti Cinta', NOW() + INTERVAL 5 DAY, 10, 100, NOW() - INTERVAL 3 DAY, NOW() - INTERVAL 1 HOUR, NOW() + INTERVAL 1 DAY, NOW() + INTERVAL 2 DAY, 'OPEN'),

-- EVENT 3: Fase Official SUDAH TUTUP, Kuota 5 (Over Quota/Bloodbath)
(3, 'Gadis-Gadis Remaja', NOW() + INTERVAL 5 DAY, 5, 100, NOW() - INTERVAL 3 DAY, NOW() - INTERVAL 1 HOUR, NOW() + INTERVAL 1 DAY, NOW() + INTERVAL 2 DAY, 'OPEN');

-- =========================================================================
-- 5. INSERT TICKET REGISTRATIONS (Status: PENDING)
-- Menggunakan ID statis (1 sampai 19) agar bisa dilacak di tabel transaksi
-- =========================================================================
INSERT INTO ticket_registrations (id_ticket_registration, id_user, id_event, phase, status, point_spent, registered_at) VALUES
-- User 3 di Event 1
(1, 3, 1, 'OFFICIAL', 'PENDING', 100, NOW()),
-- 6 Peserta di Event 2 (Under Quota)
(2, 10, 2, 'OFFICIAL', 'PENDING', 100, NOW()),
(3, 11, 2, 'OFFICIAL', 'PENDING', 100, NOW()),
(4, 12, 2, 'OFFICIAL', 'PENDING', 100, NOW()),
(5, 13, 2, 'OFFICIAL', 'PENDING', 100, NOW()),
(6, 14, 2, 'OFFICIAL', 'PENDING', 100, NOW()),
(7, 15, 2, 'OFFICIAL', 'PENDING', 100, NOW()),
-- 12 Peserta di Event 3 (Over Quota)
(8, 20, 3, 'OFFICIAL', 'PENDING', 100, NOW()),
(9, 21, 3, 'OFFICIAL', 'PENDING', 100, NOW()),
(10, 22, 3, 'OFFICIAL', 'PENDING', 100, NOW()),
(11, 23, 3, 'OFFICIAL', 'PENDING', 100, NOW()),
(12, 24, 3, 'OFFICIAL', 'PENDING', 100, NOW()),
(13, 25, 3, 'OFFICIAL', 'PENDING', 100, NOW()),
(14, 26, 3, 'OFFICIAL', 'PENDING', 100, NOW()),
(15, 27, 3, 'OFFICIAL', 'PENDING', 100, NOW()),
(16, 28, 3, 'OFFICIAL', 'PENDING', 100, NOW()),
(17, 29, 3, 'OFFICIAL', 'PENDING', 100, NOW()),
(18, 30, 3, 'OFFICIAL', 'PENDING', 100, NOW()),
(19, 31, 3, 'OFFICIAL', 'PENDING', 100, NOW());

-- =========================================================================
-- 6. INSERT POINT TRANSACTIONS
-- Melakukan mapping reference_id ke id_ticket_registration
-- =========================================================================
INSERT INTO point_transactions (id_user, amount, type, reference_id, created_at) VALUES
(3, -100, 'deduct', 1, NOW()),
(10, -100, 'deduct', 2, NOW()), (11, -100, 'deduct', 3, NOW()),
(12, -100, 'deduct', 4, NOW()), (13, -100, 'deduct', 5, NOW()),
(14, -100, 'deduct', 6, NOW()), (15, -100, 'deduct', 7, NOW()),
(20, -100, 'deduct', 8, NOW()), (21, -100, 'deduct', 9, NOW()),
(22, -100, 'deduct', 10, NOW()),(23, -100, 'deduct', 11, NOW()),
(24, -100, 'deduct', 12, NOW()),(25, -100, 'deduct', 13, NOW()),
(26, -100, 'deduct', 14, NOW()),(27, -100, 'deduct', 15, NOW()),
(28, -100, 'deduct', 16, NOW()),(29, -100, 'deduct', 17, NOW()),
(30, -100, 'deduct', 18, NOW()),(31, -100, 'deduct', 19, NOW());