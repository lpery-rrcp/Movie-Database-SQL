/*
	Insert a temp table
*/
USE Movies;

DROP TABLE IF EXISTS Movie
CREATE TABLE Movie 
(
	movie_id NUMERIC UNIQUE NOT NULL,
	movie_name VARCHAR(25) NOT NULL,
	movie_rating NUMERIC,
	release_date DATE,
	director VARCHAR(25),
	time_minutes NUMERIC,
	budget NUMERIC,
	
	CONSTRAINT movie_id_unique
		UNIQUE (movie_id),
	CONSTRAINT over_0_rating
		CHECK (movie_rating > 0)
);