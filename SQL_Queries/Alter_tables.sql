
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
