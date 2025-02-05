import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import certifi

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

if not MONGO_URI:
    raise ValueError("MongoDB URI not found in environment variables")

try:
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=10000,
        tls=True,
        tlsCAFile=certifi.where(),
        retryWrites=True,
        w='majority'
    )

    # Verify connection
    client.admin.command('ping')

    db = client["parking_management"]
    parking_records = db["parking_records"]
    
    # Create indexes
    parking_records.create_index([("license_plate", 1), ("exit_time", 1)])

except ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")
    raise
