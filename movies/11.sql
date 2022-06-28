-- list the titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated
SELECT title FROM movies, stars, people, ratings
WHERE people.id = stars.person_id
AND movies.id = stars.movie_id
AND movies.id = ratings.movie_id
AND people.name = 'Chadwick Boseman'
ORDER BY rating DESC
LIMIT 5;