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


def show_creators():
    URL = f"{BASE_URL}/person/popular?api_key={API_KEY}"
    response = requests.get(URL)
    creators = response.json()["results"]

    for creator in creators:
        print(f"- {creator['name']} (ID: {creator['id']})")


show_creators()

# Close the cursor and connection
conn.commit()

cursor.close()
conn.close()
