import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Load source
SOURCE_ES = os.getenv("SOURCE_ES")
SOURCE_USERNAME = os.getenv("SOURCE_USERNAME")
SOURCE_PASSWORD = os.getenv("SOURCE_PASSWORD")
SOURCE_AUTH = (SOURCE_USERNAME, SOURCE_PASSWORD) if SOURCE_USERNAME else None

# Load destination
DEST_ES = os.getenv("DEST_ES")
DEST_USERNAME = os.getenv("DEST_USERNAME")
DEST_PASSWORD = os.getenv("DEST_PASSWORD")
DEST_AUTH = (DEST_USERNAME, DEST_PASSWORD) if DEST_USERNAME else None

def get_indices():
    r = requests.get(f"{SOURCE_ES}/_cat/indices?h=index", auth=SOURCE_AUTH)
    r.raise_for_status()
    return [line.strip() for line in r.text.strip().split("\n") if not line.startswith(".")]

def get_index_config(index):
    r = requests.get(f"{SOURCE_ES}/{index}", auth=SOURCE_AUTH)
    r.raise_for_status()
    data = r.json()[index]
    settings = data["settings"]["index"]
    mappings = data.get("mappings", {})

    # Clean system settings
    for key in ["creation_date", "uuid", "version", "provided_name"]:
        settings.pop(key, None)

    return {
        "settings": {
            "number_of_shards": settings.get("number_of_shards", 1),
            "number_of_replicas": settings.get("number_of_replicas", 1),
            **({"analysis": settings.get("analysis")} if "analysis" in settings else {})
        },
        "mappings": mappings
    }

def create_index(dest_index, config):
    r = requests.put(f"{DEST_ES}/{dest_index}", headers={"Content-Type": "application/json"}, data=json.dumps(config), auth=DEST_AUTH)
    if not r.ok:
        print(f"[!] Failed to create index {dest_index}: {r.text}")
    else:
        print(f"[+] Created index {dest_index}")

def reindex(index):
    payload = {
        "source": {
            "remote": {
                "host": SOURCE_ES,
                "username": SOURCE_USERNAME,
                "password": SOURCE_PASSWORD
            },
            "index": index
        },
        "dest": {
            "index": index,
            "op_type": "create"
        }
    }
    r = requests.post(f"{DEST_ES}/_reindex", headers={"Content-Type": "application/json"}, data=json.dumps(payload), auth=DEST_AUTH)
    if not r.ok:
        print(f"[!] Reindex failed for {index}: {r.text}")
    else:
        print(f"[✓] Reindexed {index}")

def main():
    indices = get_indices()
    print(f"Found {len(indices)} indices: {indices}")
    for index in indices:
        print(f"\n--- Processing index: {index} ---")
        config = get_index_config(index)
        create_index(index, config)
        reindex(index)

if __name__ == "__main__":
    main()

