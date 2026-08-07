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


# Test functions
# show_actors()
insert_actors_table()

# Close the cursor and connection
conn.commit()

cursor.close()
conn.close()
