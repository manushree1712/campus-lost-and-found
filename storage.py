import json
import os
from typing import List
from models import ItemRecord

DEFAULT_FILE = "records.json"

def load_records(filepath: str = DEFAULT_FILE) -> List[ItemRecord]:
    """Loads records from JSON, auto-creating a clean template if missing or corrupted."""
    if not os.path.exists(filepath):
        save_records([], filepath)
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            if not isinstance(raw_data, list):
                raise ValueError("Root JSON element must be a list.")
            return [ItemRecord.from_dict(item) for item in raw_data]
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"[Storage Warning] Corrupted data file ({e}). Initializing clean template.")
        save_records([], filepath)
        return []

def save_records(records: List[ItemRecord], filepath: str = DEFAULT_FILE) -> None:
    """Serializes all ItemRecord objects to JSON."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump([r.to_dict() for r in records], f, indent=4)