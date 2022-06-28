--  list the names of all people who starred in a movie in which Kevin Bacon also starred
SELECT name
FROM people, movies, stars
WHERE people.id = stars.person_id
AND movies.id = stars.movie_id
AND title IN (
    SELECT title
    FROM movies, people, stars
    WHERE movies.id = stars.movie_id
    AND people.id = stars.person_id
    AND people.name = 'Kevin Bacon'
    AND people.birth = 1958
)
AND name != 'Kevin Bacon';