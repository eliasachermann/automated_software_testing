CREATE TABLE t0 (
            c0 BOOLEAN,
            c1 BLOB,
            c2 INTEGER,
            c3 INTEGER
        );
        SELECT subq10.c17 AS c8
         FROM (SELECT  TRUE AS c16, subq9.c10 AS c17
            FROM (SELECT t59.c3 AS c4, t59.c3 AS c6, t59.c2 AS c8, t59.c0 AS c10, t60.c1 AS c11, t59.c3 AS c12
               FROM t0 AS t59
                 LEFT OUTER JOIN t0 AS t60
                  ON (t59.c3 IS NOT NULL)
               ORDER BY c12) as subq9
            ORDER BY c16 ASC) as subq10
         WHERE subq10.c17 =
          CASE subq10.c16 WHEN subq10.c16 IS NULL THEN subq10.c16 END
