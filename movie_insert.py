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
    f"Driver={{{os.getenv('DRIVER_NAME')}}};"
    f"Server={os.getenv('SERVER_NAME')};"
    f"Database={os.getenv('DATABASE_NAME')};"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()


# Insert tmdb movies to the SQL Server database
cursor.execute(
    """
    SELECT * FROM Movie;
    """
)

# Checks if the table is empty
# print(cursor.fetchall())

# Check if tmdb_id already exists in the Movie table
print(response.status_code)

movies = response.json()["results"]
print(f"{(movies[1])}")

# Close the cursor and connection
conn.commit()

cursor.close()
conn.close()
