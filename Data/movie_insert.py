import os

import dotenv
from dotenv import load_dotenv
import pyodbc
import requests

# TMDB connection with API key
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = f"https://api.themoviedb.org/3"
URL = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"


response = requests.get(BASE_URL + "/movie/popular",
                        params={"api_key": API_KEY})
movies = response.json()["results"]

conn = pyodbc.connect(
    f"Driver={{{os.getenv('DRIVER_NAME')}}};"
    f"Server={os.getenv('SERVER_NAME')};"
    f"Database={os.getenv('DATABASE_NAME')};"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

movies = response.json()["results"]


def show_movies():
    for movie in movies:
        print(f"{movie['id']}, {movie['title']}")


def insert_popular_movie_table():
    URL = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"
    response = requests.get(URL)
    movies = response.json()["results"]

    # Insert movies into the Movie table
    for movie in movies:
        movie_id = movie["id"]
        title = movie["title"]
        movie_rating = movie["vote_average"]
        release_date = movie["release_date"]
        overview = movie["overview"]

        # getting the details of each movie using the movie id
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        details_response = requests.get(details_url).json()
        time_minutes = details_response["runtime"]
        budget = details_response["budget"]
        genre_name = details_response["genres"][0]["name"] if details_response["genres"] else None

        # Check if the movie already exists in the database
        cursor.execute(
            "SELECT COUNT(*) FROM Movie WHERE movie_id = ?;", (movie_id,)
        )
        count = cursor.fetchone()[0]
        if count == 0:
            print(f"Inserting: {title}")
            # Insert the movie into the database
            cursor.execute(
                "INSERT INTO Movie (movie_id, title, movie_rating, release_date, overview, time_minutes, budget) VALUES (?, ?, ?, ?, ?, ?, ?);",
                (movie_id, title, movie_rating, release_date,
                 overview, time_minutes, budget),
            )
            print(f"Inserted: {title}")
        else:
            print(f"Skipped (already exists): {title}")

        # Adds the genres of the movie into the Movie_Genre table
        for genre in movie["genre_ids"]:

            cursor.execute(
                "SELECT COUNT(*) FROM MovieGenre WHERE movie_id = ?;", (movie_id,)
            )
            print(cursor.fetchone()[0])
            # count = cursor.execute(
            #     "SELECT COUNT(*) FROM MovieGenre WHERE movie_id = ? AND genre_id = ?;", (movie_id, genre)
            # ).fetchone()[0]
            # if count == 0:
            #     cursor.execute(
            #         "INSERT INTO Movie_Genre (movie_id, genre_id) VALUES (?, ?);",
            #         (movie_id, genre),
            #     )
            #     print(
            #         f"Inserted genre ID {genre} and genre name {genre_name} for movie ID {movie_id}")
            # else:
            #     print(
            #         f"Skipped (already exists): genre ID {genre} and genre name {genre_name} for movie ID {movie_id}")


insert_popular_movie_table()
# show_movies()


# Close the cursor and connection
conn.commit()

cursor.close()
conn.close()
