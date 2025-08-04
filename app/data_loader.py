from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict
import os
from dotenv import load_dotenv
import json

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
        return [sanitize_keys(i) for i in obj]
    return obj

def save_data(entries: List[Dict], updated_at: str):
    collection.delete_many({})
    collection.insert_many(sanitize_keys(entries))
    meta.update_one({"_id": "kendra_status"}, {"$set": {"updated_at": updated_at}}, upsert=True)

def load_data(query: Dict):
    return list(collection.find(query, {"_id": 0}))

def get_status():
    status = meta.find_one({"_id": "kendra_status"})
    return {"updated_at": status.get("updated_at") if status else None}
