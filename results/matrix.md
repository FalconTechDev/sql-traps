Run: 2026-10-18T15:54:00+00:00

- mysql: 8.4.11
- mariadb: 11.8.9-MariaDB-ubu2404
- postgres: PostgreSQL 18.6 (Debian 18.6-1.pgdg13+2) on x86_64-pc-linux-gnu, compi
- mssql: Microsoft SQL Server 2022 (RTM-CU27-GDR) (KB5126934) - 16.0.4305.5 (X6

| trap / case | mysql | mariadb | postgres | mssql | differs |
|---|---|---|---|---|---|
| avg-int: AVG(x) over 1,2 | 1.5000 | 1.5000 | 1.5000000000000000 | 1 | YES |
| concat-null: 'a' || NULL | NULL | NULL | NULL | ERROR: (102, b"Incorrect syntax near '/'.DB-Lib error message 20018 | YES |
| concat-null: CONCAT('a', NULL) | NULL | NULL | a | a | YES |
| concat-null: 'a' + NULL | NULL | NULL | ERROR: operator is not unique: unknown + unknown LINE 1: SELECT 'a' | NULL | YES |
| count-star-vs-col: counts | 3,2,1 | 3,2,1 | 3,2,1 | 3,2,1 | no |
| distinct-null: SELECT DISTINCT x | 2 | 2 | 2 | 2 | no |
| distinct-null: WHERE x = x | 1 | 1 | 1 | 1 | no |
| division-by-zero: SELECT 1 / 0 | NULL | NULL | ERROR: division by zero | ERROR: (8134, b'Divide by zero error encountered.DB-Lib error messa | YES |
| fetch-with-ties: ORDER BY x FETCH FIRST 2 ROWS WITH TIES | ERROR: (1064, "You have an error in your SQL syntax; check the manu | 1; 2; 2 | 1; 2; 2 | ERROR: (153, b'Invalid usage of the option FIRST in the FETCH state | YES |
| fetch-with-ties: ORDER BY x FETCH FIRST 2 ROWS ONLY | ERROR: (1064, "You have an error in your SQL syntax; check the manu | 1; 2 | 1; 2 | ERROR: (153, b'Invalid usage of the option FIRST in the FETCH state | YES |
| group-by-nonagg: SELECT a, b ... GROUP BY a | ERROR: (1055, "Expression #2 of SELECT list is not in GROUP BY clau | 1,10 | ERROR: column "t.b" must appear in the GROUP BY clause or be used i | ERROR: (8120, b"Column 't.b' is invalid in the select list because  | YES |
| implicit-cast: '10' + 5 | 15.0 | 15.0 | 15 | 15 | YES |
| implicit-cast: '10abc' + 5 | 15.0 | 15.0 | ERROR: invalid input syntax for type integer: "10abc" LINE 1: SELEC | ERROR: (245, b"Conversion failed when converting the varchar value  | YES |
| implicit-cast: '2' > '10' (two strings) | true | true | true | true | no |
| int-overflow: 2147483647 + 1 | 2147483648 | 2147483648 | ERROR: integer out of range | ERROR: (8115, b'Arithmetic overflow error converting expression to  | YES |
| integer-division: 7 / 2 | 3.5000 | 3.5000 | 3 | 3 | YES |
| integer-division: -7 / 2 | -3.5000 | -3.5000 | -3 | -3 | YES |
| integer-division: 7 / 2.0 | 3.5000 | 3.5000 | 3.5000000000000000 | 3.500000 | YES |
| length-trailing: LENGTH('abc ') | 4 | 4 | 4 | ERROR: (195, b"'LENGTH' is not a recognized built-in function name. | YES |
| length-trailing: LEN('abc ') | ERROR: (1305, 'FUNCTION traps.LEN does not exist') | ERROR: (1305, 'FUNCTION traps.LEN does not exist') | ERROR: function len(unknown) does not exist LINE 1: SELECT LEN('abc | 3 | YES |
| not-in-null: rows of a not in b | (no rows) | (no rows) | (no rows) | (no rows) | no |
| null-order: ORDER BY x | NULL; 1; 2 | NULL; 1; 2 | 1; 2; NULL | NULL; 1; 2 | YES |
| null-order: ORDER BY x DESC | 2; 1; NULL | 2; 1; NULL | NULL; 2; 1 | 2; 1; NULL | YES |
| round-half: ROUND(2.5,0), ROUND(-2.5,0) exact | 3,-3 | 3,-3 | 3,-3 | 3.0,-3.0 | YES |
| string-compare: 'a' = 'A' | equal | equal | different | equal | YES |
| string-compare: 'a' = 'a ' (trailing space) | different | equal | different | equal | YES |
| string-compare: 'a' = ' a' (leading space) | different | different | different | different | no |
| substring-zero: SUBSTRING('abc', 0, 2) |  |  | a | a | YES |
| window-default-frame: LAST_VALUE(x) OVER (ORDER BY x) | 1,1; 2,2; 3,3 | 1,1; 2,2; 3,3 | 1,1; 2,2; 3,3 | 1,1; 2,2; 3,3 | no |