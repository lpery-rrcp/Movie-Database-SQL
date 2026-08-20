
/*Drop the table to remove the creator column*/
ALTER TABLE Movie
DROP COLUMN creator;

/*Added the budget to the Movie */
ALTER TABLE Movie
ADD budget	DECIMAL(12, 2);

/*Changes title Varchar and maximize it to 255*/
ALTER TABLE Movie
ALTER COLUMN title VARCHAR(255) NOT NULL;

/*Change show_name to title*/
ALTER TABLE Show
ALTER COLUMN title VARCHAR(255) NOT NULL;

/*Change the overview varchar to max*/
ALTER TABLE Show
ALTER COLUMN overview VARCHAR(MAX);

/*Added the total_episodes to the Shows table*/
ALTER TABLE Show
ADD total_episodes NUMERIC(18, 0)

/*Alter show rating to be be equal or greater than 0*/
ALTER TABLE Show
DROP CONSTRAINT over_0_show_rating;

ALTER TABLE Show 
ADD CONSTRAINT Show_rating_greaterOrEqual_0 CHECK (show_rating >= 0)

/*Add creative job to the Creatives table.*/
ALTER TABLE Creatives
ADD creatives_job VARCHAR(255);

/*Make the id the primary key*/
ALTER TABLE Creatives
ADD PRIMARY KEY (id);

/*Change the maximum of creatives_name from Creatives to 255*/
ALTER TABLE Creatives
ALTER COLUMN creatives_name VARCHAR(255) NOT NULL;

/*Changed the constraint "over_0_movie_rating from the Movie_genre table*/
SELECT 
    cc.name AS constraint_name,
    cc.definition
FROM sys.check_constraints cc
WHERE cc.name = 'greater_or_0_movie_rating';

ALTER TABLE Movie
DROP CONSTRAINT over_0_movie_rating;

ALTER TABLE Movie 
ADD CONSTRAINT greater_or_0_movie_rating CHECK (movie_rating >= 0);

/*Adding column row to tables MovieActor and ShowActor*/
ALTER TABLE MovieActor
ADD roles VARCHAR(255);

ALTER TABLE ShowActor
ADD roles VARCHAR(255);

/*Remove the MovieCreator table*/
DROP TABLE MovieCreator;

/*Remove the MovieCreatives Job column*/
ALTER TABLE MovieCreatives
DROP COLUMN job;

SELECT * FROM Movie;
SELECT * FROM MovieActor;
SELECT * FROM MovieCreatives;
SELECT * FROM Creatives;