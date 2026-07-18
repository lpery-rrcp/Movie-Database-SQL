import os

import dotenv
from dotenv import load_dotenv
import pyodbc
import requests

# TMDB connection with API key
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

URL = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"

response = requests.get(URL)
movies = response.json()["results"]

# for movie in movies:
#     print(f"{movie['id']}, {movie['title']}")

conn = pyodbc.connect(
    "Driver={ODBC Driver 16 for SQL Server};"
    "Server=localhost;"
    "Database=Movie;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

for movie in movies:
    movie_id = movie["id"]
    title = movie["title"]
    release_date = movie["release_date"]
    overview = movie["overview"]

    cursor.execute(
        "SELECT * FROM Movies WHERE MovieID = ?",
        (movie_id,)
    )
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO Movies (MovieID, Title, ReleaseDate, Overview) VALUES (?, ?, ?, ?)",
            (movie_id, title, release_date, overview),
        )

conn.commit()
cursor.close()
