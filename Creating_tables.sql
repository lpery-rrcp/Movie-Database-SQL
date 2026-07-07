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
	overview VARCHAR(MAX),
	creator VARCHAR(25),
	time_minutes NUMERIC,
	budget NUMERIC,
	
	CONSTRAINT movie_id_unique
		UNIQUE (movie_id),
	CONSTRAINT over_0_movie_rating
		CHECK (movie_rating > 0)
);

CREATE TABLE Show
(
	show_id NUMERIC UNIQUE NOT NULL,
	show_name VARCHAR(50) NOT NULL,
	show_rating NUMERIC,
	release_date DATE,
	overview VARCHAR(MAX),
	seasons NUMERIC,
	budget NUMERIC,

	CONSTRAINT show_id_unique
		UNIQUE (show_id),
	CONSTRAINT over_0_show_rating
		CHECK (show_rating > 0)
);