CREATE TABLE t0 (
            c2 BOOLEAN
        );
        SELECT subq1.c5 AS c6
        FROM (SELECT FALSE AS c5
           FROM (SELECT t1.c2 AS c6, t1.c2 AS c7
               FROM t0 AS t1
               ORDER BY c7 ASC
               ) as subq0
           ORDER BY c5) as subq1
        WHERE subq1.c5 =
         CASE WHEN NULLIF(subq1.c5, subq1.c5) = subq1.c5 OR subq1.c5 <>
          CASE subq1.c5 WHEN subq1.c5 = subq1.c5 THEN subq1.c5
               ELSE subq1.c5
          END THEN subq1.c5
              ELSE subq1.c5
         END;