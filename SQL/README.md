# Saikila DB exploration

## 1a. Display the first and last names of all actors from the table actor
```SQL

USE sakila;

SELECT
  first_name,
  last_name
FROM
  actor
;

```
## 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
```SQL

SELECT
  UCASE( CONCAT(first_name, ' ' , last_name) )
AS
  'Actor Name'
FROM
  actor
;

```
## 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?
```SQL

SELECT
  actor_id,
  first_name,
  last_name
FROM
  actor
WHERE
  first_name = 'Joe'
;

```
## 2b. Find all actors whose last name contain the letters GEN:
```SQL

SELECT
  first_name,
  last_name
FROM
  actor
WHERE
  last_name LIKE '%GEN%'
;

```
## 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
```SQL

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

```
## 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
```SQL

SELECT
  country_id,
  country
FROM
  country
WHERE
  country IN ('Afghanistan', 'Bangladesh', 'China' )
;

```
## 3a. Add a middle_name column to the table actor. Position it between first_name and last_name. Hint: you will need to specify the data type.
```SQL

ALTER TABLE
  actor
ADD
  middle_name VARCHAR(45) AFTER first_name
;

```
## 3b. You realize that some of these actors have tremendously long last names. Change the data type of the middle_name column to blobs.
```SQL

ALTER TABLE
  actor
MODIFY COLUMN
  middle_name BLOB
;

```
## 3c. Now delete the middle_name column.
```SQL

ALTER TABLE
  actor
DROP COLUMN
  middle_name
;

```
## 4a. List the last names of actors, as well as how many actors have that last name.
```SQL

SELECT
  last_name,
  COUNT(*)
FROM
  actor
GROUP BY
  last_name
;

```
## 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
```SQL

SELECT
  last_name,
  COUNT(*)
FROM
  actor
GROUP BY
  last_name
HAVING COUNT(*) >= 2
;

```
## 4c. Oh, no! The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS, the name of Harpo's second cousin's husband's yoga teacher. Write a query to fix the record.
```SQL

UPDATE
  actor
SET
  first_name = 'HARPO'
WHERE
 last_name = 'WILLIAMS' AND first_name = 'GROUCHO'
;

```
## 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO. Otherwise, change the first name to MUCHO GROUCHO, as that is exactly what the actor will be with the grievous error. BE CAREFUL NOT TO CHANGE THE FIRST NAME OF EVERY ACTOR TO MUCHO GROUCHO, HOWEVER! (Hint: update the record using a unique identifier.)
```SQL

UPDATE
  actor
SET first_name = IF(first_name = 'HARPO', 'GROUCHO', 'MUCHO GROUCHO')
WHERE
  actor_id = 172
;

```
## 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
Hint: https://dev.mysql.com/doc/refman/5.7/en/show-create-table.html
```SQL

SHOW CREATE TABLE address;

```
## 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:
```SQL

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

```
## 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.
```SQL

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

```
## 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.
```SQL

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

```
## 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
```SQL

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

```
## 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:
	![Total amount paid](Images/total_payment.png)
  ```SQL

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

  ```
## 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.
```SQL

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

```
## 7b. Use subqueries to display all actors who appear in the film Alone Trip.
```SQL

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
```
## 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.
```SQL

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

```
## 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as famiy films.
```SQL

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
```
## 7e. Display the most frequently rented movies in descending order.
```SQL

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

```
## 7f. Write a query to display how much business, in dollars, each store brought in.
```SQL

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

```
## 7g. Write a query to display for each store its store ID, city, and country.
```SQL

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

```
## 7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)
```SQL

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

```
## 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.
```SQL

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

```
## 8b. How would you display the view that you created in 8a?
```SQL

SELECT * FROM top_five_revenue_category;

```
## 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
```SQL

DROP VIEW top_five_revenue_category;

```
