#Sakila database exploration
USE sakila;

SELECT 
	first_name, 
    last_name
FROM
	actor
;
    
SELECT
	CONCAT(first_name, ' ' , last_name)
AS
	'Actor Name'
FROM
	actor
;

SELECT
	actor_id, 
    first_name, 
    last_name
FROM
	actor
WHERE
	first_name = 'Joe'
;

SELECT
	first_name, 
    last_name
FROM
	actor
WHERE
	last_name LIKE '%GEN%'
;

SELECT
	last_name, 
    first_name
FROM
	actor
WHERE
	last_name LIKE '%LI%'
ORDER BY
	last_name ASC,
    first_name ASC
;


SELECT 
	country_id,
    country
FROM
	country
WHERE
	country IN ('Afghanistan', 'Bangladesh', 'China' )
;

ALTER TABLE 
  actor
ADD
  middle_name VARCHAR(45) AFTER first_name
;

ALTER TABLE
  actor
MODIFY COLUMN
  middle_name BLOB
;

ALTER TABLE 
  actor
DROP COLUMN
  middle_name
;

SELECT 
  last_name,
  COUNT(*)
FROM
  actor
GROUP BY
  last_name
;

SELECT 
  last_name,
  COUNT(*)
FROM
  actor
GROUP BY
  last_name
HAVING COUNT(*) >= 2
;

SELECT * FROM actor LIMIT 5;
