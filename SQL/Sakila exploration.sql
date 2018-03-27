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
;


SELECT
  CONCAT(cos.first_name, ' ', cos.last_name) AS 'Customer Name',
  cos.email,
  addr.country
FROM
  customer cos
JOIN # joing address and customer tables
	(
	SELECT
	  ci_a.address_id,
	  co_ci.country
	FROM# join address and city tables
		(
		SELECT
		  a.address_id,
		  a.address,
		  ci.city_id
		FROM
		  city ci
		JOIN
		  address a
		WHERE
		  ci.city_id = a.city_id
		) AS ci_a
	JOIN # joing country and city tables
		(
		SELECT
		  co.country_id,
		  co.country,
		  ci.city_id,
		  ci.city
		FROM
		  country co
		JOIN
		  city ci
		WHERE country = 'Canada' AND co.country_id = ci.country_id
		)AS co_ci
	WHERE
	  ci_a.city_id = co_ci.city_id
	)AS addr
WHERE
  addr.address_id = cos.address_id
;

SELECT
  f.title,
  c.name
FROM
  film f
JOIN
  (
  SELECT
    cat.name,
    fc.film_id
  FROM
    category cat
  JOIN
    film_category fc
  WHERE
    fc.category_id = cat.category_id AND cat.name = 'Family'
  ) as c
WHERE
  f.film_id = c.film_id
;

SELECT
  film.title,
  COUNT(*) AS 'Rental_count'
FROM
  film
JOIN
(
	SELECT
	  rental.rental_id,
	  inventory.inventory_id,
	  inventory.film_id
	FROM
	  rental
	JOIN
	  inventory
	WHERE
	  rental.inventory_id = inventory.inventory_id
) AS inv
WHERE
  film.film_id = inv.film_id
GROUP BY
  film.title
ORDER BY
  Rental_count DESC
;


SELECT
  st.store_id,
  SUM(pmt.amount) AS 'Total payments'
FROM
  payment pmt
JOIN
	(
	SELECT
	  staff.staff_id,
	  store.store_id
	FROM
	  staff
	JOIN
	  store
	WHERE
	  staff.store_id = store.store_id
	) AS st
WHERE
  pmt.staff_id = st.staff_id
GROUP BY
  st.store_id
;


SELECT
  store.store_id,
  place.city,
  place.country
FROM
  store
JOIN
  (
	SELECT
	  place.country,
	  place.city,
	  address.address_id
	FROM
	  address
	JOIN
	(  
		SELECT
		  country.country,
		  city.city,
		  country.country_id,
		  city.city_id
		FROM
		  city
		JOIN
		  country
		WHERE
		  city.country_id = country.country_id
	) AS place
	WHERE
	  place.city_id = address.city_id
  ) AS place
WHERE
  store.address_id = place.address_id
;

SELECT
  category.name,
  SUM(rent.amount) AS 'Revenue'
FROM
  category
JOIN
(
	SELECT
	  rent.amount,
	  film_category.film_id,
      film_category.category_id
	FROM
	  film_category
	JOIN
	(
		SELECT
		  inventory.inventory_id,
		  inventory.film_id,
		  rent.rental_id,
		  rent.amount
		FROM
		  inventory
		JOIN
		(
			SELECT 
			  payment.amount,
			  rental.inventory_id,
			  payment.rental_id
			FROM 
			  payment
			JOIN
			  rental
			WHERE
			  payment.rental_id = rental.rental_id
		) AS rent
		WHERE
		  inventory.inventory_id = rent.inventory_id
	) AS rent
	WHERE
	  film_category.film_id = rent.film_id
) AS rent
WHERE
  category.category_id = rent.category_id
GROUP BY
  category.name
ORDER BY Revenue DESC
LIMIT 5
;


CREATE VIEW top_five_revenue_category AS
SELECT
  category.name,
  SUM(rent.amount) AS 'Revenue'
FROM
  category
JOIN
(
	SELECT
	  rent.amount,
	  film_category.film_id,
      film_category.category_id
	FROM
	  film_category
	JOIN
	(
		SELECT
		  inventory.inventory_id,
		  inventory.film_id,
		  rent.rental_id,
		  rent.amount
		FROM
		  inventory
		JOIN
		(
			SELECT 
			  payment.amount,
			  rental.inventory_id,
			  payment.rental_id
			FROM 
			  payment
			JOIN
			  rental
			WHERE
			  payment.rental_id = rental.rental_id
		) AS rent
		WHERE
		  inventory.inventory_id = rent.inventory_id
	) AS rent
	WHERE
	  film_category.film_id = rent.film_id
) AS rent
WHERE
  category.category_id = rent.category_id
GROUP BY
  category.name
ORDER BY Revenue DESC
LIMIT 5
;

SELECT * FROM top_five_revenue_category;

DROP VIEW top_five_revenue_category;