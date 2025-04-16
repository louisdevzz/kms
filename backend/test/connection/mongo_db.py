from pymongo import MongoClient
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
import certifi
load_dotenv()

username = quote_plus(os.getenv("MONGODB_USERNAME"))
password = quote_plus(os.getenv("MONGODB_PASSWORD"))
cluster = os.getenv("MONGODB_CLUSTER")
db_name = os.getenv("MONGODB_DB_NAME")

uri = f"mongodb+srv://{username}:{password}@{cluster}/{db_name}?retryWrites=true&w=majority"

client = MongoClient(uri, tlsCAFile=certifi.where())
try:
    # Ping the server
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print("❌ Connection failed:", e)
finally:
    client.close()
