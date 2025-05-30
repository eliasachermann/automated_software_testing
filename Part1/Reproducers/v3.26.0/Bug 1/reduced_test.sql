CREATE TABLE IF NOT EXISTS t_qEeX3Lyy (
    c_KWx REAL,
    c_Q2FI INTEGER,
    c_i8t INTEGER,
    c_wr05oYEJ INTEGER,
    c_ROb INTEGER,
    c_0R7QqM REAL DEFAULT -216820.16,
    c_1AoL8a4cZg TEXT DEFAULT 'nqlRc55YTF2DM3d8CO0',
    PRIMARY KEY (c_0R7QqM)
);


INSERT OR REPLACE INTO t_qEeX3Lyy (c_KWx, c_Q2FI, c_i8t, c_wr05oYEJ, c_ROb, c_0R7QqM, c_1AoL8a4cZg)
    VALUES
    (982885.1, 37144803, 39382906, 39575084, 40643132, -383008.072, 'QY_4241'),
    (660472.461, 136847859, 137444454, 139763708, 140482910, 379861.107, 'YWRIWDhmZzix_14241');


INSERT OR REPLACE INTO t_qEeX3Lyy (c_KWx, c_Q2FI, c_i8t, c_wr05oYEJ, c_ROb, c_0R7QqM, c_1AoL8a4cZg)
    SELECT 74015.326138, 36769432, 39215613, 39411927, 40777807, 920499.0035, 'xOTb5qbxqeLem5SdN5rh_4241';

SELECT
    SUBSTR((FALSE = t_qEeX3Lyy.c_wr05oYEJ), HEX(t_qEeX3Lyy.c_Q2FI)),
    +(t_qEeX3Lyy.c_KWx GLOB t_qEeX3Lyy.c_Q2FI)
FROM t_qEeX3Lyy
WHERE t_qEeX3Lyy.c_ROb
ORDER BY 1;