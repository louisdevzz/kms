from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
from backend.utils.config_loader import get_db_config

load_dotenv()

config = get_db_config()
uri = config['uri']
db_name = config['db_name']

# Connect to MongoDB
client = MongoClient(uri, tlsCAFile=certifi.where())
try:
    # Ping the server
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")

    db = client[db_name]

    collections = db.list_collection_names()
    print("📁 Collections in the database:")
    for name in collections:
        print(f" - {name}")

except Exception as e:
    print("❌ Connection failed:", e)
finally:
    client.close()
