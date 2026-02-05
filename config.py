from dotenv import load_dotenv
import os

load_dotenv()


USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")
DATABASE = os.getenv("POSTGRES_DB")

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")



SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")