CREATE TABLE IF NOT EXISTS t_gEyw (c_y8ZqZFAD REAL, c_pWxRfRyK NUMERIC, c_ZHFBa REAL, c_vWfV3aj INTEGER PRIMARY KEY, c_dZ9J INTEGER DEFAULT 509870, c_6Eq INTEGER, c_oEs0qY TEXT, c_25YFOj2o1M NUMERIC, c_JHn7AR REAL, c_68hZi8I NUMERIC DEFAULT -770690, UNIQUE (c_JHn7AR, c_y8ZqZFAD, c_6Eq), FOREIGN KEY (c_pWxRfRyK) REFERENCES t_PFkQi(c_v745v));
CREATE TEMP TABLE t_ihbRwl92 (c_4Ypv REAL, c_G1fXcCjz6g INTEGER DEFAULT 246587);
CREATE TABLE IF NOT EXISTS t_6I8aUl (c_rSihIYV TEXT, c_gQlar2h TEXT DEFAULT '7Lfa6OvoJGq4d', c_0Za TEXT, UNIQUE (c_gQlar2h, c_rSihIYV, c_0Za), FOREIGN KEY (c_0Za) REFERENCES t_1XICi(c_k2YPr));
CREATE TABLE t_hmgX (c_jx413v9W TEXT PRIMARY KEY, UNIQUE (c_jx413v9W), FOREIGN KEY (c_jx413v9W) REFERENCES t_Xu5JM(c_tnNum));
ALTER TABLE t_hmgX RENAME COLUMN c_jx413v9W TO c_FIJwkt;
ALTER TABLE t_gEyw RENAME TO t_zfaHpiJ;
ALTER TABLE t_ihbRwl92 RENAME COLUMN c_G1fXcCjz6g TO c_pxCOqLD;

                CREATE TRIGGER trg_wI5gA
                AFTER INSERT ON t_ihbRwl92
                BEGIN
                    SELECT RAISE(IGNORE) WHERE (SELECT count(*) FROM t_ihbRwl92) > 1000;
                END;

                CREATE TRIGGER trg_uz5TH
                AFTER DELETE ON t_6I8aUl
                BEGIN
                    SELECT RAISE(IGNORE) WHERE (SELECT count(*) FROM t_6I8aUl) > 1000;
                END;

                CREATE TRIGGER trg_B98CQ
                AFTER DELETE ON t_hmgX
                BEGIN
                    SELECT RAISE(IGNORE) WHERE (SELECT count(*) FROM t_hmgX) > 1000;
                END;
INSERT OR IGNORE INTO t_ihbRwl92 (c_4Ypv, c_pxCOqLD) SELECT -601677.93628, 10683464;
INSERT OR IGNORE INTO t_6I8aUl (c_rSihIYV, c_gQlar2h, c_0Za) VALUES ('kvTOEeKzkbU9V_966', 'h8IXb9z_1066', '9tIpFjEEoQ4Kk39jlF_1166');
WITH cte_hML AS (SELECT 1) INSERT OR REPLACE INTO t_6I8aUl (c_rSihIYV, c_gQlar2h, c_0Za) VALUES ('4N3ajepJ2MfFvg0_966', '0rFQOpT1ib1_1066', 'BqlPBEBlGxaHHvdqu_1166');
INSERT OR IGNORE INTO t_hmgX (c_FIJwkt) VALUES ('i_966');
INSERT OR REPLACE INTO t_zfaHpiJ (c_y8ZqZFAD, c_pWxRfRyK, c_ZHFBa, c_vWfV3aj, c_dZ9J, c_6Eq, c_oEs0qY, c_25YFOj2o1M, c_JHn7AR, c_68hZi8I) VALUES (-17436.720877, 10852055, -956042.53, 13025973, 13757547, 14840005, 'qZ0JTz5Z0ASvZ_1566', 16779708, 547401.2, 18260314), (-54815.206999999995, 109931363, 226653.19, 112581690, 113806965, 114494539, 'h7LM6OIapHyUKpZjnaP_11566', 116907489, 229636.70117000001, 117936633);
WITH cte_EKx AS (SELECT 1) REPLACE INTO t_zfaHpiJ (c_y8ZqZFAD, c_pWxRfRyK, c_ZHFBa, c_vWfV3aj, c_dZ9J, c_6Eq, c_oEs0qY, c_25YFOj2o1M, c_JHn7AR, c_68hZi8I) SELECT 261408.08, 11257495, -214926.362, 12009609, 14391657, 14011966, 'KrzNTDtSab8AD_1566', 17112379, -194147.4, 18740771;
REPLACE INTO t_zfaHpiJ (c_y8ZqZFAD, c_pWxRfRyK, c_ZHFBa, c_vWfV3aj, c_dZ9J, c_6Eq, c_oEs0qY, c_25YFOj2o1M, c_JHn7AR, c_68hZi8I) VALUES (122423.05114, 10053030, -962139.9, 12850894, 13583730, 15166497, 'jhk1dtAgQ1OeLWbmf2Ov_1566', 16882151, 290161.5968, 18705240);
REPLACE INTO t_zfaHpiJ (c_y8ZqZFAD, c_pWxRfRyK, c_ZHFBa, c_vWfV3aj, c_dZ9J, c_6Eq, c_oEs0qY, c_25YFOj2o1M, c_JHn7AR, c_68hZi8I) VALUES (-715580.88863, 10330007, -557552.749, 11867821, 14499952, 14979365, 'Uxgol6G1FG8whlKBbdop_1566', 16795720, 311984.68788, 18084689);
REPLACE INTO t_zfaHpiJ (c_y8ZqZFAD, c_pWxRfRyK, c_ZHFBa, c_vWfV3aj, c_dZ9J, c_6Eq, c_oEs0qY, c_25YFOj2o1M, c_JHn7AR, c_68hZi8I) SELECT 742015.178852, 11271143, -354633.52, 12055206, 13032545, 15349661, 'SezU_1566', 16425417, -714611.206122, 19154635;
BEGIN TRANSACTION;
UPDATE OR IGNORE t_ihbRwl92 SET c_4Ypv = -497 WHERE ROWID = (SELECT MIN(ROWID) FROM t_ihbRwl92);
UPDATE OR IGNORE t_ihbRwl92 SET c_pxCOqLD = NULL WHERE ROWID = (SELECT MIN(ROWID) FROM t_ihbRwl92);
COMMIT;

WITH RECURSIVE counter(n) AS (
    SELECT MIN(CASE WHEN typeof(c_rSihIYV) IN ('integer','real') THEN c_rSihIYV ELSE 0 END) FROM t_6I8aUl
    UNION ALL
    SELECT n+1 FROM counter 
    WHERE n < (SELECT MIN(100,MAX(CASE WHEN typeof(c_rSihIYV) IN ('integer','real') THEN c_rSihIYV ELSE 10 END)) FROM t_6I8aUl)
)
SELECT n, COUNT(*) AS count_matches 
FROM counter 
LEFT JOIN t_6I8aUl ON counter.n = CASE WHEN typeof(c_rSihIYV) IN ('integer','real') THEN c_rSihIYV ELSE NULL END
GROUP BY n
ORDER BY n
LIMIT 20;

SELECT json_set('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":6, "f":null}, "g":true, "h":false, "i":[{"j":10},{"j":20}]}', '$.a', 100) as modified_a,
    json_set('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":6, "f":null}, "g":true, "h":false, "i":[{"j":10},{"j":20}]}', '$.d.e', 200) as modified_nested,
    json_set('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":6, "f":null}, "g":true, "h":false, "i":[{"j":10},{"j":20}]}', '$.d.new', 'new value') as added_property,
    json_set('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":6, "f":null}, "g":true, "h":false, "i":[{"j":10},{"j":20}]}', '$.c[1]', 99) as modified_array,
    json_insert('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":6, "f":null}, "g":true, "h":false, "i":[{"j":10},{"j":20}]}', '$.j', 'inserted') as inserted_j,
    json_insert('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":6, "f":null}, "g":true, "h":false, "i":[{"j":10},{"j":20}]}', '$.a', 'ignored') as insert_existing,
    json_replace('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":6, "f":null}, "g":true, "h":false, "i":[{"j":10},{"j":20}]}', '$.a', 999) as replaced_a,
    json_replace('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":6, "f":null}, "g":true, "h":false, "i":[{"j":10},{"j":20}]}', '$.nonexistent', 'ignored') as replace_nonexistent,
    json_remove('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":6, "f":null}, "g":true, "h":false, "i":[{"j":10},{"j":20}]}', '$.d') as removed_d,
    json_remove('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":6, "f":null}, "g":true, "h":false, "i":[{"j":10},{"j":20}]}', '$.c[0]') as removed_array_element,
    json_patch('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":6, "f":null}, "g":true, "h":false, "i":[{"j":10},{"j":20}]}', '{"a":null, "z":100}') as patched
FROM t_zfaHpiJ
LIMIT 1;

SELECT DISTINCT t_6I8aUl.c_gQlar2h, c_rSihIYV IN (SELECT t_6I8aUl.c_rSihIYV FROM t_6I8aUl LIMIT 5) FROM t_6I8aUl ORDER BY 1;