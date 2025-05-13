CREATE TABLE IF NOT EXISTS t_iewuWVNq (c_Tj7 TEXT DEFAULT 'I' COLLATE NOCASE, c_Vs0nZMvRzx INTEGER PRIMARY KEY, c_JnoLvZjl TEXT, c_wUu3V6W REAL DEFAULT NULL, c_4SzcpJ5ST8 INTEGER, c_e1O NUMERIC, c_BVB2h NUMERIC, c_CD6Bs INTEGER DEFAULT -543927, c_hgJIDBgT6 INTEGER) WITHOUT ROWID;
CREATE TABLE t_Xyu (c_21eJYdiFy INTEGER, c_n6c5hc REAL, c_MFypdxjXAx INTEGER, c_sSUxpZhXc NUMERIC, c_yapl TEXT, c_Sl0cx7Uk TEXT, c_ffJueOiR6K NUMERIC, c_XY9t NUMERIC, c_S7DHhU NUMERIC, c_Voo TEXT);
CREATE TEMP TABLE t_PlHmKl (c_hQMGvw REAL, c_IxbqXWZPOO NUMERIC DEFAULT 726052, c_ZkSWeUZm6k TEXT, c_2OfTFjg REAL, c_y6o REAL, c_Qe48EGc1 NUMERIC, c_0aGlkiOO6u NUMERIC DEFAULT -514673, c_HZbLtjRNl TEXT, PRIMARY KEY (c_hQMGvw, c_ZkSWeUZm6k), UNIQUE (c_HZbLtjRNl));
ALTER TABLE t_PlHmKl RENAME COLUMN c_ZkSWeUZm6k TO c_bLiztb;
ALTER TABLE t_PlHmKl RENAME TO t_rcZX;
INSERT OR REPLACE INTO t_iewuWVNq (c_Tj7, c_Vs0nZMvRzx, c_JnoLvZjl, c_wUu3V6W, c_4SzcpJ5ST8, c_e1O, c_BVB2h, c_CD6Bs, c_hgJIDBgT6) SELECT 'VfO1akwEhn_7490', 75004317, 'SfsnWdcqVL77BDgzghvP_7690', -407593.7, 79750852, 79836208, 81476776, 82696903, 81932686;
REPLACE INTO t_iewuWVNq (c_Tj7, c_Vs0nZMvRzx, c_JnoLvZjl, c_wUu3V6W, c_4SzcpJ5ST8, c_e1O, c_BVB2h, c_CD6Bs, c_hgJIDBgT6) VALUES ('uR2crVmmEQa_7490', 76795942, 'o_7690', 27732.720139999998, 79335036, 80626784, 80576312, 82233763, 83292738);
INSERT OR IGNORE INTO t_Xyu (c_21eJYdiFy, c_n6c5hc, c_MFypdxjXAx, c_sSUxpZhXc, c_yapl, c_Sl0cx7Uk, c_ffJueOiR6K, c_XY9t, c_S7DHhU, c_Voo) VALUES (74525686, 110797.157699, 77204387, 77480116, 'zwFhoSvayY3tUx_7890', 'iUx_7990', 81554356, 82452407, 82876616, 'SYhmHWoKHs_8390');
REPLACE INTO t_Xyu (c_21eJYdiFy, c_n6c5hc, c_MFypdxjXAx, c_sSUxpZhXc, c_yapl, c_Sl0cx7Uk, c_ffJueOiR6K, c_XY9t, c_S7DHhU, c_Voo) VALUES (74892094, 175717.21000000002, 77729271, 78075236, 'SdGVev3gaP_7890', 'FTsPoJijE_7990', 80173437, 81895722, 83464247, 'EyiyN_8390'), (174421088, 411656.22479999997, 176132717, 177337494, 'skv_17890', 'tP1TfR6FRtU76SEu_17990', 180256056, 182665071, 182790278, 'CxDObvSo7zSm7ZZtoWvU_18390');
REPLACE INTO t_rcZX (c_hQMGvw, c_IxbqXWZPOO, c_bLiztb, c_2OfTFjg, c_y6o, c_Qe48EGc1, c_0aGlkiOO6u, c_HZbLtjRNl) VALUES (286780.5, 76229016, 'JnX_7690', 890789.407171, 674245.28014, 79299057, 80835235, 'VWBHSEEQn4_8190');
INSERT OR REPLACE INTO t_rcZX (c_hQMGvw, c_IxbqXWZPOO, c_bLiztb, c_2OfTFjg, c_y6o, c_Qe48EGc1, c_0aGlkiOO6u, c_HZbLtjRNl) SELECT 178179.74599999998, 76419849, 'Eixv2_7690', 434161.045, 458775.80641, 80735332, 79942267, 'NmueO8FMHKNR8afBPRd_8190';
INSERT OR FAIL INTO t_rcZX DEFAULT VALUES;
BEGIN TRANSACTION;
INSERT OR REPLACE INTO t_iewuWVNq (c_Tj7, c_Vs0nZMvRzx, c_JnoLvZjl, c_wUu3V6W, c_4SzcpJ5ST8, c_e1O, c_BVB2h, c_CD6Bs, c_hgJIDBgT6) VALUES ('lap9_7490', 75420559, 'ebDw_7690', 225428.2, 77920252, 80646631, 81572181, 82621268, 82041734);
UPDATE OR IGNORE t_iewuWVNq SET c_e1O = -879 WHERE c_Tj7 IS NOT NULL;
REPLACE INTO t_iewuWVNq (c_Tj7, c_Vs0nZMvRzx, c_JnoLvZjl, c_wUu3V6W, c_4SzcpJ5ST8, c_e1O, c_BVB2h, c_CD6Bs, c_hgJIDBgT6) VALUES ('I9o_7490', 75040550, '3UdrtYIhMNx1fMv1q4g_7690', -852046.98908, 79705487, 79762306, 79956387, 81778667, 82096290), ('OXhvI_17490', 175661208, 'O0CDi_17690', 1010160.558, 178962860, 180470550, 181385624, 182189552, 182704159);
COMMIT;

WITH json_data(id, data) AS (
    SELECT c_Tj7, '{"a":1, "b":"text", "c":[3,4,5], "d":{"e":6, "f":null}, "g":true, "h":false, "i":[{"j":10},{"j":20}]}'
    FROM t_iewuWVNq
    LIMIT 10
)
SELECT id,
    json_extract(data, '$.a') as a_value,
    json_extract(data, '$.b') as b_value,
    json_extract(data, '$.c') as c_array,
    SUM(json_extract(data, '$.a')) OVER () as sum_a,
    AVG(json_extract(data, '$.a')) OVER () as avg_a,
    json_group_array(json_extract(data, '$.a')) OVER () as all_a_values,
    json_group_object(id, json_extract(data, '$.b')) OVER () as id_to_b_map
FROM json_data
ORDER BY id;


SELECT 
    t1.c_0aGlkiOO6u,
    (SELECT COUNT(*) FROM t_rcZX t2 WHERE t2.c_0aGlkiOO6u = t1.c_0aGlkiOO6u) as same_value_count,
    CASE WHEN EXISTS(SELECT 1 FROM t_rcZX t3 WHERE t3.c_0aGlkiOO6u > t1.c_0aGlkiOO6u LIMIT 1) 
        THEN 'Not Max' ELSE 'Max' END as is_max_value,
    (SELECT COUNT(*) FROM (
        SELECT DISTINCT c_0aGlkiOO6u FROM t_rcZX
    )) as distinct_values_count
FROM t_rcZX t1
WHERE t1.c_0aGlkiOO6u IN (
    SELECT c_0aGlkiOO6u 
    FROM t_rcZX 
    WHERE typeof(c_0aGlkiOO6u) NOT IN ('null')
    GROUP BY c_0aGlkiOO6u
    HAVING COUNT(*) > 0
)
ORDER BY (SELECT COUNT(*) FROM t_rcZX t4 WHERE t4.c_0aGlkiOO6u = t1.c_0aGlkiOO6u) DESC
LIMIT 10;

SELECT t_iewuWVNq.c_wUu3V6W, t_iewuWVNq.c_hgJIDBgT6, t_iewuWVNq.c_e1O, t_iewuWVNq.c_CD6Bs, LOWER(t_iewuWVNq.c_CD6Bs) AS computed_c_CD6Bs FROM t_iewuWVNq LIMIT 10;
SELECT CASE CASE t_rcZX.c_0aGlkiOO6u WHEN t_rcZX.c_hQMGvw THEN t_rcZX.c_y6o WHEN t_rcZX.c_0aGlkiOO6u THEN t_rcZX.c_bLiztb ELSE t_rcZX.c_2OfTFjg END WHEN NOT t_rcZX.c_HZbLtjRNl THEN CASE t_rcZX.c_IxbqXWZPOO WHEN t_rcZX.c_y6o THEN t_rcZX.c_IxbqXWZPOO WHEN t_rcZX.c_hQMGvw THEN t_rcZX.c_0aGlkiOO6u ELSE 349100 END WHEN CASE x'066E' WHEN t_rcZX.c_HZbLtjRNl THEN -464831 WHEN t_rcZX.c_2OfTFjg THEN t_rcZX.c_IxbqXWZPOO ELSE FALSE END THEN ~ t_rcZX.c_hQMGvw WHEN NULL THEN t_rcZX.c_bLiztb END, FALSE AS alias_9IY, c_IxbqXWZPOO FROM t_rcZX WHERE (LOWER(t_rcZX.c_2OfTFjg) < NOT NULL) EXCEPT SELECT c_HZbLtjRNl, c_CD6Bs, t_iewuWVNq.c_hgJIDBgT6 FROM t_iewuWVNq JOIN t_rcZX ON t_iewuWVNq.c_Vs0nZMvRzx = t_rcZX.c_y6o WHERE t_iewuWVNq.c_e1O ORDER BY 1 ASC;

SELECT DISTINCT t_rcZX.c_Qe48EGc1,
COUNT(*) OVER (PARTITION BY t_rcZX.c_2OfTFjg) as window_count,
RANK() OVER (ORDER BY CASE WHEN typeof(t_rcZX.c_Qe48EGc1) IN ('null') THEN 0 
                        ELSE t_rcZX.c_Qe48EGc1 END DESC) as rank_val,
CASE WHEN t_rcZX.c_Qe48EGc1 IS NULL THEN 'Unknown' ELSE 'Known' END as status
FROM t_rcZX
WHERE t_rcZX.c_Qe48EGc1 IS NOT NULL
GROUP BY t_rcZX.c_Qe48EGc1, t_rcZX.c_2OfTFjg
HAVING COUNT(*) > 0
ORDER BY window_count DESC
LIMIT 20;


SELECT t_rcZX.c_Qe48EGc1,
t_rcZX.c_2OfTFjg,
SUM(CASE WHEN typeof(t_rcZX.c_Qe48EGc1) IN ('integer', 'real', 'numeric') THEN t_rcZX.c_Qe48EGc1 ELSE 0 END) 
    OVER (PARTITION BY t_rcZX.c_2OfTFjg) as window_total
FROM t_rcZX
GROUP BY t_rcZX.c_Qe48EGc1, t_rcZX.c_2OfTFjg
HAVING SUM(CASE WHEN typeof(t_rcZX.c_Qe48EGc1) IN ('integer', 'real', 'numeric') THEN t_rcZX.c_Qe48EGc1 ELSE 0 END) > 0
ORDER BY window_total DESC
LIMIT 10;