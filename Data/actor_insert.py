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


def show_actors():
    URL = f"{BASE_URL}/person/popular?api_key={API_KEY}"
    response = requests.get(URL)
    actors = response.json()["results"]

    for actor in actors:
        print(f"- {actor['name']} (ID: {actor['id']})")


def insert_actors_table():
    URL = f"{BASE_URL}/person/popular?api_key={API_KEY}"
    response = requests.get(URL)
    actors = response.json()["results"]

    for actor in actors:
        actor_id = actor["id"]
        actor_name = actor["name"]

        # Check if the actor already exists in the database
        cursor.execute(
            "SELECT COUNT(*) FROM Actor WHERE id = ?;", (actor_id,)
        )
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute(
                "INSERT INTO Actor (id, actor_name) VALUES (?, ?);",
                (actor_id, actor_name)
            )
            print(f"Inserting: {actor_name} (ID: {actor_id})")
        else:
            print(f"Skipped (already exists): {actor_name} (ID: {actor_id})")
            continue


def insert_MovieActor():
    URL = f"{BASE_URL}/person/popular?api_key={API_KEY}"
    response = requests.get(URL)
    actors = response.json()["results"]

    for actor in actors:
        actor_id = actor["id"]
        # Add the data into the MovieActor table
        movie_url = f"{BASE_URL}/person/{actor_id}/movie_credits?api_key={API_KEY}"
        movie_response = requests.get(movie_url)
        movie_credits = movie_response.json().get("cast", [])

    for movie in movie_credits:
        movie_id = movie["id"]
        roles = ", ".join([credit["character"]
                          for credit in movie_credits if credit["id"] == movie_id])

        # cursor.execute(
        #     "INSERT INTO MovieActor (movie_id, actor_id, roles) VALUES (?, ?, ?);",
        #     (movie_id, actor_id, roles)
        # )
        print(
            f"Inserted into MovieActor: Movie ID {movie_id}, Actor ID {actor_id}, Roles: {roles}")


# Test functions
# show_actors()
# insert_actors_table()
insert_MovieActor()

# Close the cursor and connection
conn.commit()

cursor.close()
conn.close()
