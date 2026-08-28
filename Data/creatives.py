# Trying to get the director, writer, and producer of the movie using the movie id. I will use the credits endpoint of the TMDB API to get this information. The credits endpoint provides information about the cast and crew of a movie, including the director, writer, and producer.

import os

import dotenv
from dotenv import load_dotenv
import pyodbc
import requests

# TMDB connection with API key
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = f"https://api.themoviedb.org/3"

conn = pyodbc.connect(
    f"Driver={{{os.getenv('DRIVER_NAME')}}};"
    f"Server={os.getenv('SERVER_NAME')};"
    f"Database={os.getenv('DATABASE_NAME')};"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()


def show_people():
    # show the director, writer, and producer of the movie using the movie id. I will use the credits endpoint of the TMDB API to get this information. The credits endpoint provides information about the cast and crew of a movie, including the director, writer, and producer.
    URL = f"{BASE_URL}/movie/popular?api_key={API_KEY}"
    response = requests.get(URL)
    movies = response.json()["results"]

    for movie in movies:
        movie_id = movie["id"]
        title = movie["title"]
        URL = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"
        response = requests.get(URL)
        credits = response.json()

        director = None
        writer = None
        producer = None

        for crew_member in credits["crew"]:
            if crew_member["job"] == "Director":
                director = crew_member["name"]
            elif crew_member["job"] == "Writer":
                writer = crew_member["name"]
            elif crew_member["job"] == "Producer":
                producer = crew_member["name"]
        print(
            f"- {title} (ID: {movie_id}) (Director: {director}, Writer: {writer}, Producer: {producer})")


def insert_people(id, name, job):
    # Check if the creative already exists in the database
    cursor.execute(
        "SELECT COUNT(*) FROM Creatives WHERE id = ?;", (id,)
    )
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute(
            "INSERT INTO Creatives (id, creatives_name, creatives_job) VALUES (?, ?, ?)",
            (id, name, job),
        )
        print(f"Inserting: {name} (ID: {id}, Job: {job})")
    else:
        print(f"Skipped (already exists): {name} (ID: {id}, Job: {job})")


def insert_people_movie():
    # insert the director, writer, and producer of the movie using the movie id. I will use the credits endpoint of the TMDB API to get this information. The credits endpoint provides information about the cast and crew of a movie, including the director, writer, and producer.
    URL = f"{BASE_URL}/movie/popular?api_key={API_KEY}"
    response = requests.get(URL)
    movies = response.json()["results"]

    for movie in movies:
        movie_id = movie["id"]
        URL = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"
        response = requests.get(URL)
        credits = response.json()

        for crew_member in credits["crew"]:
            job = crew_member["job"]

            if job in ["Director", "Writer", "Producer"]:
                creative_id = crew_member["id"]
                creative_name = crew_member["name"]
                creatives_id = crew_member["id"]

                # Check if the creative already exists in the database
                insert_people(creative_id, creative_name, job)


def insert_MovieCreatives():
    # Add the data into the MovieCreatives table
    URL = f"{BASE_URL}/movie/popular?api_key={API_KEY}"
    response = requests.get(URL)
    movies = response.json()["results"]

    for movie in movies:
        movie_id = movie["id"]
        movie_title = movie["title"]
        movie_rating = movie.get("vote_average")
        release_date = movie.get("release_date")
        movie_overview = movie.get("overview")
        # details
        movie_details_url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}"
        movie_details_response = requests.get(movie_details_url)
        movie_time = movie_details_response.json().get("runtime")
        movie_budget = movie_details_response.json().get("budget")

        URL = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"
        response = requests.get(URL)
        credits = response.json()
        print(f"Processing movie ID: {movie_id}")
        print(f"Creatives: {credits['crew']}")

        # Check if the movie exists in the Movie table
        movie_count = cursor.execute(
            "SELECT COUNT(*) FROM Movie WHERE movie_id = ?;", (movie_id,)
        ).fetchone()[0]

        if movie_count == 0:
            print(
                f"Movie ID {movie_id} does not exist in the Movie table. Skipping.")
            # Add the movie to the Movie table before adding creatives
            cursor.execute(
                "INSERT INTO Movie (movie_id, title, movie_rating, release_date, overview, time_minutes, budget) VALUES (?, ?, ?, ?, ?, ?, ?);",
                (movie_id, movie_title, movie_rating, release_date,
                 movie_overview, movie_time, movie_budget)
            )
            print(f"Inserted movie ID {movie_id} into the Movie table.")
            continue
        else:
            print(
                f"Movie ID {movie_id} exists in the Movie table. Proceeding to insert creatives.")

        # Check if the creative exists in the Creative table
        for crew_member in credits["crew"]:
            job = crew_member["job"]

            if job in ["Director", "Writer", "Producer"]:
                creative_id = crew_member["id"]
                creative_name = crew_member["name"]

                cursor.execute(
                    "SELECT COUNT(*) FROM Creatives WHERE id = ?;", (creative_id,)
                )
                count = cursor.fetchone()[0]

                insert_people(creative_id, creative_name, job)

                # Check if the movie-creative relationship already exists
                cursor.execute(
                    "SELECT COUNT(*) FROM MovieCreatives WHERE movie_id = ? AND creative_id = ?;",
                    (movie_id, creative_id),
                )
                count = cursor.fetchone()[0]

                if count == 0:
                    cursor.execute(
                        "INSERT INTO MovieCreatives (movie_id, creative_id) VALUES (?, ?);",
                        (movie_id, creative_id),
                    )
                    print(
                        f"Inserted movie ID {movie_id} and creative ID {creative_id} into the MovieCreatives table.")
                else:
                    print(
                        f"Skipped (already exists): movie ID {movie_id} and creative ID {creative_id} in the MovieCreatives table.")


def insert_people_show():
    # insert the director, writer, and producer of the show using the show id. I will use the credits endpoint of the TMDB API to get this information. The credits endpoint provides information about the cast and crew of a show, including the director, writer, and producer.
    URL = f"{BASE_URL}/tv/popular?api_key={API_KEY}"
    response = requests.get(URL)
    shows = response.json()["results"]

    for show in shows:
        show_id = show["id"]
        URL = f"{BASE_URL}/tv/{show_id}/credits?api_key={API_KEY}"
        response = requests.get(URL)
        credits = response.json()

        for crew_member in credits["crew"]:
            job = crew_member["job"]

            if job in ["Director", "Writer", "Producer"]:
                creative_id = crew_member["id"]
                creative_name = crew_member["name"]
                creatives_id = crew_member["id"]

                # Check if the creative already exists in the database
                cursor.execute(
                    "SELECT COUNT(*) FROM Creatives WHERE id = ?;", (creative_id,)
                )
                count = cursor.fetchone()[0]

                if count == 0:
                    cursor.execute(
                        "INSERT INTO Creatives (id, creatives_name, creatives_job) VALUES (?, ?, ?)",
                        (creative_id, creative_name, job),
                    )
                    print(
                        f"Inserting: {creative_name} (ID: {creatives_id}, Job: {job})")
                else:
                    print(
                        f"Skipped (already exists): {creative_name} (ID: {creative_id}, Job: {job})")
                    continue


# Function testing
# show_people()
# insert_people_movie()
# insert_people_show()
insert_MovieCreatives()
# insert_people(100, "test", "Director")

# close the cursor and connection
conn.commit()
cursor.close()
conn.close()
