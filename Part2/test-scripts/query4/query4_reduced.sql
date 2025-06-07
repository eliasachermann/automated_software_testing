CREATE TABLE t1 (col2 text, col4 text ); 
INSERT INTO t1 (col2,col4) VALUES ('AHX', 'TPudz8'); 
INSERT INTO t1 (col4) VALUES ('Kbre8p'); 

SELECT LAG(403961669) OVER () AS win0, AVG(t1.col2) OVER (PARTITION BY col4) AS win1, ROW_NUMBER() OVER () AS win2 FROM t1;
