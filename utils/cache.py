import hashlib
import json
import os

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

memory_cache = {}

def _hash_key(key: str) -> str:
    return hashlib.md5(key.encode()).hexdigest()

def get_cache(key: str):
    if key in memory_cache:
        return memory_cache[key]

    path = f"{CACHE_DIR}/{_hash_key(key)}.json"

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            memory_cache[key] = data
            return data

    return None

def set_cache(key: str, value):
    memory_cache[key] = value

    path = f"{CACHE_DIR}/{_hash_key(key)}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False)