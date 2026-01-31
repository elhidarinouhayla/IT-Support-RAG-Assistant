from dotenv import load_dotenv
import os

load_dotenv()


USER=os.getenv("DB_USER")
PASSWORD=os.getenv("PASSWORD")
PORT=os.getenv("PORT")
HOST=os.getenv("HOST")
DB_NAME=os.getenv("DB_NAME")

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")