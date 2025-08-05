from datetime import datetime
from typing import Dict
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["kendraDB"]         
collection = db["kendras"]      
meta = db["metadata"]         

def sanitize_keys(obj):
    if isinstance(obj, dict):
        return {k.replace('.', '_'): sanitize_keys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_keys(item) for item in obj]
    else:
        return obj

def load_data(query: Dict = None) -> Dict:
    updated = meta.find_one({"_id": "kendra_update"})
    updated_at = updated["updated_at"] if updated else None

    if query:
        results = list(collection.find(query, {"_id": 0}))
    else:
        results = list(collection.find({}, {"_id": 0}))

    return {
        "updated_at": updated_at,
        "results": results
    }

def save_data(entries, updated_at: str = None, batch_size: int = 750, reset: bool = False):
    """
    Save Kendra entries into MongoDB.
    - If reset=True: clear old data and overwrite metadata timestamp.
    - If reset=False: append new entries, keep old data and timestamp.
    Accepts either a list or a generator.
    """
    if reset:
        collection.delete_many({})
        if updated_at is None:
            updated_at = datetime.now().isoformat()
    else:
        updated_at = None

    batch = []
    for entry in entries:
        batch.append(sanitize_keys(entry))
        if len(batch) >= batch_size:
            collection.insert_many(batch)
            batch = []

    if batch:
        collection.insert_many(batch)

    if reset:
        meta.update_one(
            {"_id": "kendra_update"},
            {"$set": {"updated_at": updated_at}},
            upsert=True
        )