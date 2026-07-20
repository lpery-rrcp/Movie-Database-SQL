ALTER TABLE Movie
DROP COLUMN creator;

ALTER TABLE Movie
ADD budget	DECIMAL(12, 2);

SELECT * FROM Movie;