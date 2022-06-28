-- list the titles of all movies in which both Johnny Depp and Helena Bonham Carter starred.
SELECT title
FROM movies, people, stars
WHERE movies.id = stars.movie_id
AND people.id = stars.person_id
AND people.name = 'Johnny Depp'
AND title IN (
    SELECT title
    FROM movies, people, stars
    WHERE movies.id = stars.movie_id
    AND people.id = stars.person_id
    AND people.name = 'Helena Bonham Carter'
);