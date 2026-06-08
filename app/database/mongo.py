from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path=".env")

# Ambil Mongo URL
MONGO_URL = os.getenv("MONGO_URL")

# Ambil nama database
MONGO_DB = os.getenv("MONGO_DB")

print(MONGO_URL)
print(MONGO_DB)

# Connect MongoDB
client = MongoClient(MONGO_URL)

# Pilih database
mongodb = client[MONGO_DB]