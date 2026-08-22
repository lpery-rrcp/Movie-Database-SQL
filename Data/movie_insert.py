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


def insert_movies(movie_id):
    # getting the details of each movie using the movie id
    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    details_response = requests.get(details_url).json()
    movie_id = details_response["id"]
    title = details_response["title"]
    movie_rating = details_response["vote_average"]
    release_date = details_response["release_date"]
    overview = details_response["overview"]
    time_minutes = details_response["runtime"]
    budget = details_response["budget"]
    # print(f"Inserting: {title}")
    # print(f"Movie ID: {movie_id}, Title: {title}, Rating: {movie_rating}, Release Date: {release_date}, Overview: {overview}, Runtime: {time_minutes}, Budget: {budget}")

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
             overview, time_minutes, budget)
        )
        print(f"Inserted: {title}")
    else:
        print(f"Skipped (already exists): {title}")


def insert_popular_movie_table():
    URL = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"
    response = requests.get(URL)
    movies = response.json()["results"]

    # Insert movies into the Movie table
    for movie in movies:
        movie_id = movie["id"]

        insert_movies(movie_id)

        # getting the details of each movie to get the genre
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        details_response = requests.get(details_url).json()
        genre_name = details_response["genres"][0]["name"] if details_response["genres"] else None

        # Adds the genres of the movie into the Movie_Genre table
        for genre in movie["genre_ids"]:
            print(
                f"Adding genre ID {genre} and genre name {genre_name} for movie ID {movie_id}")
            cursor.execute(
                "SELECT COUNT(*) FROM MovieGenre WHERE movie_id = ?;", (movie_id,)
            )

            count = cursor.execute(
                "SELECT COUNT(*) FROM MovieGenre WHERE movie_id = ? AND genre_id = ?;", (movie_id, genre)
            ).fetchone()[0]

            if count == 0:
                cursor.execute(
                    "INSERT INTO MovieGenre (movie_id, genre_id) VALUES (?, ?);",
                    (movie_id, genre),
                )
                print(
                    f"Inserted genre ID {genre} and genre name {genre_name} for movie ID {movie_id}")
            else:
                print(
                    f"Skipped (already exists): genre ID {genre} and genre name {genre_name} for movie ID {movie_id}")


def insert_MovieActor():
    URL = f"{BASE_URL}/person/popular?api_key={API_KEY}"
    response = requests.get(URL)
    actors = response.json()["results"]
    print("Start")

    for actor in actors:
        actor_id = actor["id"]

        # Add the data into the MovieActor table
        movie_url = f"{BASE_URL}/person/{actor_id}/movie_credits?api_key={API_KEY}"
        movie_response = requests.get(movie_url)
        movie_credits = movie_response.json().get("cast", [])

        counter = 0

        for movie in movie_credits:
            movie_id = movie["id"]
            title = movie["title"]
            movie_rating = movie["vote_average"]
            release_date = movie["release_date"]
            overview = movie["overview"]
            roles = movie.get("character", "")

            # Check if movie_id exists in the Movie table
            print(
                f"Checking if movie ID {movie_id} exists in the Movie table for actor ID {actor_id}")

            cursor.execute(
                "SELECT COUNT(*) FROM Movie WHERE movie_id = ?;", (movie_id,)
            )
            movie_exists = cursor.fetchone()[0] > 0

            if movie_exists == 0:
                # the movie does not exist in the Movie table, so insert it

                # getting the details of each movie using the movie id
                details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
                details_response = requests.get(details_url).json()
                time_minutes = details_response["runtime"]
                budget = details_response["budget"]

                # Insert the movie into the Movie table
                cursor.execute(
                    "INSERT INTO Movie (movie_id, title, movie_rating, release_date, overview, time_minutes, budget) VALUES (?, ?, ?, ?, ?, ?, ?);",
                    (movie_id, title, movie_rating, release_date,
                     overview, time_minutes, budget)
                )
                print(f"Inserted movie: {movie['title']} (ID: {movie_id})")
            else:
                print(
                    f"Movie ID {movie_id} already exists in the Movie table.")

            # Check if the actor exists in the Actor table
            cursor.execute(
                "SELECT COUNT(*) FROM Actor WHERE id = ?;", (actor_id,)
            )
            actor_exists = cursor.fetchone()[0] > 0

            if not actor_exists:
                # Insert the actor into the Actor table
                cursor.execute(
                    "INSERT INTO Actor (id, actor_name) VALUES (?, ?);",
                    (actor_id, actor["name"])
                )
                print(
                    f"Inserted actor: {actor['name']} (ID: {actor_id})")
            else:
                print(
                    f"Actor ID {actor_id} already exists in the Actor table.")

            # # check if the movie-actor relationship already exists in the database
            cursor.execute(
                "SELECT COUNT(*) FROM MovieActor WHERE movie_id = ? AND actor_id = ?;",
                (movie_id, actor_id)
            )

            if cursor.fetchone()[0] == 0:
                # Insert the movie-actor relationship into the database
                cursor.execute(
                    "INSERT INTO MovieActor (movie_id, actor_id, roles) VALUES (?, ?, ?);",
                    (movie_id, actor_id, roles)
                )
                print(
                    f"Inserted into MovieActor: Movie ID {movie_id}, Actor ID {actor_id}, Roles: {roles}")
            else:
                print(
                    f"Skipped (already exists in MovieActor): Movie ID {movie_id}, Actor ID {actor_id}, Roles: {roles}")

            # Count movies processed for this actor
            counter += 1

            if counter >= 2:
                print(
                    f"Reached 2 movies for actor {actor_id}"
                )
                break


insert_popular_movie_table()
# show_movies()
# insert_MovieActor()
# inset_movie_id = 550  # Example movie ID for testing
# insert_movies(inset_movie_id)

# Close the cursor and connection
conn.commit()

cursor.close()
conn.close()
