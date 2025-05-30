CREATE TABLE T1(c1 REAL, c2 JSON, c3 REAL NOT NULL DEFAULT NULL);
CREATE TABLE T2(c1 JSON);
CREATE TABLE T3(c1 NUMERIC, c2 BLOB);
INSERT INTO T1(c1, c2, c3) VALUES (933, '{"k": 4}', -131);
INSERT INTO T1(c1, c2, c3) VALUES (953, '{"k": 2}', 851);
INSERT INTO T1(c1, c2, c3) VALUES (722, '{"k": 5}', 679);
INSERT INTO T2(c1) VALUES ('{"k": 6}');
INSERT INTO T2(c1) VALUES ('{"k": 7}');
INSERT INTO T2(c1) VALUES ('{"k": 9}');
INSERT INTO T3(c1, c2) VALUES (-325, 411);
INSERT INTO T3(c1, c2) VALUES (182, 41);
INSERT INTO T3(c1, c2) VALUES (564, 406);
SELECT DISTINCT c.c2, b.c1, 491 FROM T1 AS a LEFT JOIN T2 AS b ON a.c3 = b.c1 LEFT JOIN T3 AS c ON b.c1 = c.c2 WHERE c.c1 > a.c3;
