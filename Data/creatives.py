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
insert_people_show()
# close the cursor and connection
conn.commit()
cursor.close()
conn.close()
