CREATE TABLE t_E96o (c_0I4 INTEGER, UNIQUE (c_0I4));
REPLACE INTO t_E96o (c_0I4) SELECT 74464467;
REPLACE INTO t_E96o (c_0I4) VALUES (74134102);
INSERT OR REPLACE INTO t_E96o (c_0I4) SELECT 73869720;
WITH cte_Wc1 AS (SELECT 1) REPLACE INTO t_E96o (c_0I4) VALUES (74756084), (174387953);
INSERT OR REPLACE INTO t_E96o (c_0I4) VALUES (74347122);
SELECT * FROM t_E96o;
SELECT json_extract('{"a":1, "b":2, "c":[3,4,5], "d":{"e":6}}', '$.a') as simple_extract,
json_extract('{"a":1, "b":2, "c":[3,4,5], "d":{"e":6}}', '$.c[1]') as array_extract,
json_extract('{"a":1, "b":2, "c":[3,4,5], "d":{"e":6}}', '$.d.e') as nested_extract,
json_type('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":null}}', '$.a') as type_number,
json_type('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":null}}', '$.b') as type_text,
json_type('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":null}}', '$.c') as type_array,
json_type('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":null}}', '$.d') as type_object,
json_type('{"a":1, "b":"text", "c":[3,4,5], "d":{"e":null}}', '$.d.e') as type_null,
json_array(1, 'text', NULL, 3.14, json_object('key', 'value')) as created_array,
json_object('a', 1, 'b', 'text', 'c', NULL, 'd', json_array(1,2,3)) as created_object
FROM t_E96o
ORDER BY 1
LIMIT 1;
SELECT t_E96o.c_0I4 FROM t_E96o ORDER BY t_E96o.c_0I4 DESC LIMIT 10;
SELECT ((t_E96o.c_0I4 <> t_E96o.c_0I4) | ROUND(t_E96o.c_0I4, t_E96o.c_0I4)), c_0I4 FROM t_E96o WHERE ((t_E96o.c_0I4 <= t_E96o.c_0I4) OR t_E96o.c_0I4) GROUP BY c_0I4 ORDER BY 1 ASC;

SELECT DISTINCT t_E96o.c_0I4,
    COUNT(*) OVER (PARTITION BY t_E96o.c_0I4) as window_count,
    RANK() OVER (ORDER BY CASE WHEN typeof(t_E96o.c_0I4) IN ('null') THEN 0 
                            ELSE t_E96o.c_0I4 END DESC) as rank_val,
    CASE WHEN t_E96o.c_0I4 IS NULL THEN 'Unknown' ELSE 'Known' END as status
FROM t_E96o
WHERE t_E96o.c_0I4 IS NOT NULL
GROUP BY t_E96o.c_0I4, t_E96o.c_0I4
HAVING COUNT(*) > 0
ORDER BY window_count DESC
LIMIT 20;


SELECT t_E96o.c_0I4,
    t_E96o.c_0I4,
    SUM(CASE WHEN typeof(t_E96o.c_0I4) IN ('integer', 'real', 'numeric') THEN t_E96o.c_0I4 ELSE 0 END) 
        OVER (PARTITION BY t_E96o.c_0I4) as window_total
FROM t_E96o
GROUP BY t_E96o.c_0I4, t_E96o.c_0I4
HAVING SUM(CASE WHEN typeof(t_E96o.c_0I4) IN ('integer', 'real', 'numeric') THEN t_E96o.c_0I4 ELSE 0 END) > 0
ORDER BY window_total DESC
LIMIT 10;