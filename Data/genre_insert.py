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


def insert_genre_table():
    URL = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}"
    response = requests.get(URL)
    genres = response.json()["genres"]

    # Show the genres retrieved from the API
    print("Genres retrieved from the API:")
    for genre in genres:
        print(f"- {genre['name']} (ID: {genre['id']})")

    # for genre in genres:
    #     genre_id = genre["id"]
    #     genre_name = genre["name"]

    #     cursor.execute(
    #         "INSERT INTO Genre (genre_id, genre_name) VALUES (?, ?);",
    #         (genre_id, genre_name)
    #     )


insert_genre_table()

# Close the cursor and connection
conn.commit()

cursor.close()
conn.close()
