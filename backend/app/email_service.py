from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB URI
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file")

# MongoDB Connection
client = MongoClient(MONGO_URI)

# Database Name
db = client["SubZy"]


def get_db():
    return db