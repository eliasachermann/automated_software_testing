CREATE TABLE t0 (
    c0 BOOLEAN,
    c1 INTEGER,
    c2 BOOLEAN,
    c3 TEXT,
    c4 NULL,
    c5 INTEGER,
    c6 BOOLEAN
);

SELECT subq1.c13
FROM (SELECT FALSE AS c13
   FROM (SELECT t1.c2 AS c9, t1.c5 AS c11
      FROM t0 AS t1
      ORDER BY c9 ASC
      ) as subq0
   ORDER BY c13 ASC) as subq1
WHERE subq1.c13 = 
 CASE subq1.c13 WHEN subq1.c13 = subq1.c13 THEN subq1.c13
      ELSE subq1.c13
 END OR subq1.c13 = NULLIF(subq1.c13, subq1.c13) OR subq1.c13 IS NOT NULL AND subq1.c13 = subq1.c13

