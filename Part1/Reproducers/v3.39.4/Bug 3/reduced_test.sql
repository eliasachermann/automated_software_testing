CREATE TABLE IF NOT EXISTS t_vTWs (c_0ypdsmDA NUMERIC, c_QVh REAL, c_n17Cl REAL DEFAULT -859057.3, c_rt0fvz64FE NUMERIC, UNIQUE (c_rt0fvz64FE));
CREATE TABLE IF NOT EXISTS t_1NuG (c_Uyjo INTEGER, c_nYbHuyScU INTEGER, c_7nwk9Bu NUMERIC);
CREATE TABLE IF NOT EXISTS t_n9rpE (c_Pg98oN TEXT, c_Q9gEFUXU INTEGER DEFAULT 610448, c_XyEBI REAL, c_S2BWQJL INTEGER, c_8z4 INTEGER, c_9gpdQef TEXT, c_tzr2PnxOn REAL, c_6VVMxzVx INTEGER, c_43zKb REAL);
REPLACE INTO t_vTWs (c_0ypdsmDA, c_QVh, c_n17Cl, c_rt0fvz64FE) VALUES (77929761, -546055.4, -391595.96, 79817770), (177981812, 563936.72, 401559.1, 181058416);
INSERT OR REPLACE INTO t_vTWs (c_0ypdsmDA, c_QVh, c_n17Cl, c_rt0fvz64FE) VALUES (77636165, -717989.42, -888898.037585, 81155864), (177406467, 778326.42288, 758980.43187, 180527672);
INSERT OR IGNORE INTO t_vTWs (c_0ypdsmDA, c_QVh, c_n17Cl, c_rt0fvz64FE) VALUES (76766748, 1047564.8, 321791.22, 81501446), (177404923, -531397.17, 605160.298, 179756371);
REPLACE INTO t_vTWs (c_0ypdsmDA, c_QVh, c_n17Cl, c_rt0fvz64FE) VALUES (77576900, -610709.95296, 96022.20999999999, 81516728), (176976362, -399313.228, -435741.51939000003, 181098951);
REPLACE INTO t_vTWs (c_0ypdsmDA, c_QVh, c_n17Cl, c_rt0fvz64FE) VALUES (78048374, -778749.71446, -677530.24, 80832180), (177011431, -134753.09000000003, -74527.74437999999, 179612483);
INSERT OR REPLACE INTO t_1NuG (c_Uyjo, c_nYbHuyScU, c_7nwk9Bu) VALUES (78357386, 79111831, 78829513);
WITH cte_3H7 AS (SELECT 1) INSERT OR IGNORE INTO t_1NuG (c_Uyjo, c_nYbHuyScU, c_7nwk9Bu) VALUES (78127967, 78236089, 78746245), (176734751, 177944914, 178873420);
INSERT OR REPLACE INTO t_1NuG (c_Uyjo, c_nYbHuyScU, c_7nwk9Bu) VALUES (77914341, 79127564, 79261170);
INSERT OR IGNORE INTO t_1NuG (c_Uyjo, c_nYbHuyScU, c_7nwk9Bu) VALUES (77555665, 79315397, 78845239), (177046412, 178850129, 180292826);
WITH cte_h4W AS (SELECT 1) INSERT OR REPLACE INTO t_1NuG (c_Uyjo, c_nYbHuyScU, c_7nwk9Bu) VALUES (77117485, 79477995, 79757302);
REPLACE INTO t_n9rpE (c_Pg98oN, c_Q9gEFUXU, c_XyEBI, c_S2BWQJL, c_8z4, c_9gpdQef, c_tzr2PnxOn, c_6VVMxzVx, c_43zKb) VALUES ('EUPCuwpx3ZJHG16txX_7756', 78830082, 243079.36461, 81487199, 81677921, '9beYA4DNgVPNLO_8256', -492533.449, 84466932, -722296.34624);
REPLACE INTO t_n9rpE (c_Pg98oN, c_Q9gEFUXU, c_XyEBI, c_S2BWQJL, c_8z4, c_9gpdQef, c_tzr2PnxOn, c_6VVMxzVx, c_43zKb) VALUES ('GY3pz4mi9pBsf1Dd_7756', 77745398, -143107.737, 80218845, 81753619, 'eZsILsLhNuJ_8256', 728766.3, 85386773, 87339.59);
BEGIN TRANSACTION;
UPDATE OR IGNORE t_1NuG SET c_nYbHuyScU = NULL WHERE ROWID = (SELECT MIN(ROWID) FROM t_1NuG);
UPDATE OR IGNORE t_1NuG SET c_Uyjo = -544 WHERE ROWID = (SELECT MIN(ROWID) FROM t_1NuG);
COMMIT;
SELECT DISTINCT CASE WHEN c_0ypdsmDA THEN QUOTE(t_vTWs.c_QVh) WHEN NOT t_1NuG.c_7nwk9Bu THEN TIME(t_1NuG.c_nYbHuyScU, t_1NuG.c_7nwk9Bu, t_1NuG.c_nYbHuyScU) END AS alias_Aqt, CASE WHEN (t_vTWs.c_QVh < NULL) THEN CASE WHEN t_vTWs.c_0ypdsmDA THEN t_1NuG.c_nYbHuyScU WHEN TRUE THEN t_vTWs.c_0ypdsmDA ELSE t_1NuG.c_nYbHuyScU END WHEN TRUE THEN (t_1NuG.c_Uyjo = -327288) END, * FROM t_n9rpE, t_vTWs, t_1NuG ORDER BY 1 LIMIT 1;