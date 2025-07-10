import json
import os

CONFIG_FILE = "config.json"

def save_config(data: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def get_store_id():
    config = load_config()
    return config.get("store_id")

def set_store_id(store_id: str):
    config = load_config()
    config["store_id"] = store_id
    save_config(config)
