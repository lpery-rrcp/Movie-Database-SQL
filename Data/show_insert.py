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


def insert_shows_table():
    URL = f"{BASE_URL}/tv/popular?api_key={API_KEY}"
    response = requests.get(URL)
    shows = response.json()["results"]

    for show in shows:
        show_id = show["id"]
        show_name = show["name"]

        # Fetch additional details for each show
        details_url = f"{BASE_URL}/tv/{show_id}?api_key={API_KEY}"
        details_response = requests.get(details_url)
        details = details_response.json()

        # Extract additional details
        show_rating = details.get("vote_average")
        release_date = details.get("first_air_date")
        overview = details.get("overview")
        seasons = details.get("number_of_seasons")
        budget = details.get("budget")
        episodes = details.get("number_of_episodes")
        print(f"Show ID: {show_id}, Name: {show_name}, Rating: {show_rating}, Release Date: {release_date}, Overview: {overview}, Seasons: {seasons}, Budget: {budget}, Episodes: {episodes}")

        # # Check if the show already exists in the database
        # cursor.execute(
        #     "SELECT COUNT(*) FROM Show WHERE id = ?;", (show_id,)
        # )
        # count = cursor.fetchone()[0]
        # if count == 0:
        #     cursor.execute(
        #         "INSERT INTO Show (id, show_name) VALUES (?, ?, ?, ?, ?);",
        #         (show_id, show_name, show_rating, release_date, overview, seasons, budget)
        #     )
        #     print(f"Inserting: {show_name} (ID: {show_id})")
        # else:
        #     print(f"Skipped (already exists): {show_name} (ID: {show_id})")
        #     continue


# Function calls
# show_shows()
insert_shows_table()
# Close the cursor and connection
conn.commit()

cursor.close()
conn.close()
