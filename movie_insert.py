import os

import dotenv
from dotenv import load_dotenv

import requests

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

URL = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"

response = requests.get(URL)
movies = response.json()["results"]

for movie in movies:
    print(f"{movie['id']}, {movie['title']}")
