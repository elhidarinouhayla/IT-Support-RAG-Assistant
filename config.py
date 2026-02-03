from dotenv import load_dotenv
import os

load_dotenv()


USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
PORT=os.getenv("PORT")
HOST=os.getenv("HOST")
DATABASE=os.getenv("DATABASE")

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")



SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")