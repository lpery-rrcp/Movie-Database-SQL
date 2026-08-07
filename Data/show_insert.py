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


def show_shows():
    URL = f"{BASE_URL}/tv/popular?api_key={API_KEY}"
    response = requests.get(URL)
    shows = response.json()["results"]

    for show in shows:
        print(f"- {show['name']} (ID: {show['id']})")


# Fucntion calls
show_shows()

# Close the cursor and connection
conn.commit()

cursor.close()
conn.close()
