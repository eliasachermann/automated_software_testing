CREATE TABLE F (p BOOLEAN NOT NULL, i BOOLEAN);
INSERT INTO F SELECT * FROM (VALUES ((NOT false), false), (NULL, true))
WHERE (false);