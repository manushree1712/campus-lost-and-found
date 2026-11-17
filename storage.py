# storage.py
import csv
import json
import os
from datetime import datetime
from typing import List, Tuple
from models import ItemRecord, CATEGORIES, RECORD_TYPES, STATUSES

DEFAULT_FILE = "records.json"
CSV_FIELDS = ["record_id", "record_type", "item_name", "category", "location", "date_reported", "description", "contact", "status", "date_claimed"]

def load_records(filepath: str = DEFAULT_FILE) -> List[ItemRecord]:
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
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump([r.to_dict() for r in records], f, indent=4)

def export_to_csv(records: List[ItemRecord], filepath: str = "records_export.csv") -> None:
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for r in records:
            writer.writerow(r.to_dict())

def import_from_csv(filepath: str) -> Tuple[List[ItemRecord], List[str]]:
    """Imports valid records from CSV and logs row-level validation errors."""
    valid_records, errors = [], []
    if not os.path.exists(filepath):
        return valid_records, [f"File '{filepath}' not found."]

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            try:
                rec_type = row["record_type"].strip().upper()
                cat = row["category"].strip()
                status = row.get("status", "OPEN").strip().upper()
                datetime.strptime(row["date_reported"].strip(), "%Y-%m-%d")

                if rec_type not in RECORD_TYPES or cat not in CATEGORIES or status not in STATUSES:
                    raise ValueError("Invalid type, category, or status.")
                if len(row["item_name"].strip()) < 2:
                    raise ValueError("Item name too short.")

                valid_records.append(ItemRecord(
                    record_id=row["record_id"].strip(),
                    record_type=rec_type,
                    item_name=row["item_name"].strip(),
                    category=cat,
                    location=row["location"].strip(),
                    date_reported=row["date_reported"].strip(),
                    description=row.get("description", "").strip(),
                    contact=row["contact"].strip(),
                    status=status,
                    date_claimed=row.get("date_claimed") or None
                ))
            except Exception as e:
                errors.append(f"Row {row_num}: {e}")
    return valid_records, errors