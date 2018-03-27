#Sakila database exploration
USE sakila;

SELECT 
	first_name, 
    last_name
FROM
	actor
;
    
SELECT
	  UCASE( CONCAT(first_name, ' ' , last_name) )
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

UPDATE
  actor
SET
  first_name = 'HARPO'
WHERE
 last_name = 'WILLIAMS' AND first_name = 'GROUCHO'
;
  
UPDATE
  actor
SET first_name = IF(first_name = 'HARPO', 'GROUCHO', 'MUCHO GROUCHO')
WHERE
  actor_id = 172
;

SHOW CREATE TABLE address;

SELECT
  s.first_name,
  s.last_name,
  a.address
FROM 
  address a
INNER JOIN
  staff s
WHERE
  s.address_id = a.address_id
;

SELECT
  s.first_name,
  SUM(p.amount) AS 'Total'
FROM
  staff s
INNER JOIN
  payment p
WHERE
  s.staff_id = p.staff_id 
  AND p.payment_date > '2005-08-01 00:00:00' AND p.payment_date < '2005-08-31 23:59:59'  
GROUP BY
  s.first_name
;

SELECT
  f.title,
  COUNT(*)
FROM
  film f
INNER JOIN 
  film_actor
WHERE
  f.film_id = film_actor.film_id
GROUP BY 
  f.title
;

  
SELECT
  f.title,
  COUNT(i.inventory_id) AS 'No of copies'
FROM
  film f
INNER JOIN
  inventory i
WHERE
  f.film_id = i.film_id AND f.title = 'Hunchback Impossible'
GROUP BY
  f.title
;

SELECT
  c.last_name,
  SUM(p.amount) AS 'Total Amount Paid'
FROM
  customer c
INNER JOIN
  payment p
WHERE
  c.customer_id = p.customer_id
GROUP BY
  c.last_name
ORDER BY
  c.last_name ASC
;

SELECT
  title
FROM
  film
WHERE
  title LIKE 'K%' OR title LIKE 'Q%' 
  AND language_id 
  IN
  (
    SELECT 
      language_id
	FROM
      language
	WHERE
      name = 'English'
  )
;

SELECT
  CONCAT(actor.first_name, ' ', actor.last_name)
AS
  'Actor Name'
FROM
  actor
WHERE
  actor_id IN
  (
    SELECT
      actor_id
    FROM
      film_actor
    WHERE 
      film_id IN
      (
      SELECT
        film_id
      FROM
        film
      WHERE
        title = 'Alone Trip'
      )
  )
