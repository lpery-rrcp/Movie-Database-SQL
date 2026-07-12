import os

import dotenv
from dotenv import load_dotenv

import requests

load_dotenv()
print(f"TMDB_API_KEY: {os.getenv('TMDB_API_KEY')}")
