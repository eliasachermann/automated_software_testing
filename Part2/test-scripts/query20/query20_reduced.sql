CREATE TABLE t0 (
    c0 BOOLEAN,
    c1 BOOLEAN
);
SELECT subq1.c8
FROM (SELECT TRUE AS c8
   FROM (SELECT t1.c1 AS c5, t1.c0 AS c6, t1.c0 AS c7
      FROM t0 AS t1
      WHERE t1.c1 = t1.c0
      ORDER BY c5
      ) as subq0
   ORDER BY c8) as subq1
WHERE subq1.c8 <> 
 CASE subq1.c8 
  WHEN subq1.c8 = CASE subq1.c8 
                    WHEN subq1.c8 = subq1.c8
                    THEN subq1.c8 
                    ELSE subq1.c8 
                  END 
  THEN subq1.c8 
  ELSE subq1.c8 
END


