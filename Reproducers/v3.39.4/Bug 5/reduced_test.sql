CREATE TABLE IF NOT EXISTS t_iewuWVNq (c_Tj7 TEXT DEFAULT 'I' COLLATE NOCASE, c_Vs0nZMvRzx INTEGER PRIMARY KEY, c_JnoLvZjl TEXT, c_wUu3V6W REAL DEFAULT NULL, c_4SzcpJ5ST8 INTEGER, c_e1O NUMERIC, c_BVB2h NUMERIC, c_CD6Bs INTEGER DEFAULT -543927, c_hgJIDBgT6 INTEGER) WITHOUT ROWID;

INSERT OR REPLACE INTO t_iewuWVNq (c_Tj7, c_Vs0nZMvRzx, c_JnoLvZjl, c_wUu3V6W, c_4SzcpJ5ST8, c_e1O, c_BVB2h, c_CD6Bs, c_hgJIDBgT6) SELECT 'VfO1akwEhn_7490', 75004317, 'SfsnWdcqVL77BDgzghvP_7690', -407593.7, 79750852, 79836208, 81476776, 82696903, 81932686;
REPLACE INTO t_iewuWVNq (c_Tj7, c_Vs0nZMvRzx, c_JnoLvZjl, c_wUu3V6W, c_4SzcpJ5ST8, c_e1O, c_BVB2h, c_CD6Bs, c_hgJIDBgT6) VALUES ('uR2crVmmEQa_7490', 76795942, 'o_7690', 27732.720139999998, 79335036, 80626784, 80576312, 82233763, 83292738);


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