/*
	Insert a temp table
*/
USE Movies;

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

CREATE TABLE Genre
(
	id NUMERIC UNIQUE NOT NULL,
	genre_name VARCHAR(25) NOT NULL,
);

CREATE TABLE Actor
(
	id NUMERIC UNIQUE NOT NULL,
	actor_name VARCHAR(25) NOT NULL,
);

CREATE TABLE Creator 
(
	id NUMERIC UNIQUE NOT NULL,
	creator_name VARCHAR(25) NOT NULL,
);

/* Mixed table */

/*for genres??*/
CREATE TABLE MovieGenre
(
	movie_id NUMERIC NOT NULL,
	genre_id NUMERIC NOT NULL,

	CONSTRAINT fk_movie
	FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
	CONSTRAINT fk_genre
	FOREIGN KEY (genre_id) REFERENCES Genre(id)
);

CREATE TABLE ShowGenre
(
	show_id NUMERIC NOT NULL,
	genre_id NUMERIC NOT NULL,

	CONSTRAINT fk_show_genre
	FOREIGN KEY (show_id) REFERENCES Show(show_id),
	CONSTRAINT fk_genre_show
	FOREIGN KEY (genre_id) REFERENCES Genre(id)
);

CREATE TABLE MovieActor
(
	movie_id NUMERIC NOT NULL,
	actor_id NUMERIC NOT NULL,

	CONSTRAINT fk_movie_actor_id
	FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
	CONSTRAINT fk_actor_movie_id
	FOREIGN KEY (actor_id) REFERENCES Actor(id), 
);