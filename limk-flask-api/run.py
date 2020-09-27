# run.py
from app import create_app
from dotenv import load_dotenv

# the path to your .env file (or any other file of environment variables you want to load)
load_dotenv('.env')

app = create_app()
