from datetime import datetime
from typing import List, Dict
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

def save_data(entries: List[Dict], updated_at: str = None):
    if updated_at is None:
        updated_at = datetime.now().isoformat()
    collection.delete_many({})
    if entries:
        sanitized = [sanitize_keys(entry) for entry in entries]
        collection.insert_many(sanitized)

    meta.update_one(
        {"_id": "kendra_update"},
        {"$set": {"updated_at": updated_at}},
        upsert=True
    )
