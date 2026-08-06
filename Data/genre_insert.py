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


def show_genres():
    URL = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}"
    response = requests.get(URL)
    genres = response.json()["genres"]

    for genre in genres:
        print(f"- {genre['name']} (ID: {genre['id']})")


def insert_genre_table():
    URL = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}"
    response = requests.get(URL)
    genres = response.json()["genres"]

    for genre in genres:
        genre_id = genre["id"]
        genre_name = genre["name"]

        # Check if the genre already exists in the database
        cursor.execute(
            "SELECT COUNT(*) FROM Genre WHERE id = ?;", (genre_id,)
        )
        if cursor.fetchone()[0] == 0:
            print(f"Inserting: {genre_name} (ID: {genre_id})")

            cursor.execute(
                "INSERT INTO Genre (id, genre_name) VALUES (?, ?);",
                (genre_id, genre_name)
            )
        else:
            print(f"Skipped (already exists): {genre_name} (ID: {genre_id})")


# Fucntion calls
# show_genres()
insert_genre_table()

# Close the cursor and connection
conn.commit()

cursor.close()
conn.close()
