from collections import Counter
from datetime import datetime
from typing import List, Dict
from models import ItemRecord

def generate_next_id(records: List[ItemRecord], record_type: str) -> str:
    prefix = "LST" if record_type == "LOST" else "FND"
    return f"{prefix}-{len(records) + 1:04d}"

def find_potential_matches(new_item: ItemRecord, records: List[ItemRecord]) -> List[ItemRecord]:
    """Finds OPEN records of the opposite type with matching category or keyword overlap."""
    target_type = "FOUND" if new_item.record_type == "LOST" else "LOST"
    new_words = set(new_item.item_name.lower().split())
    matches = []

    for r in records:
        if r.record_type == target_type and r.status == "OPEN":
            existing_words = set(r.item_name.lower().split())
            if r.category == new_item.category and (new_words & existing_words):
                matches.append(r)
    return matches

def search_records(records: List[ItemRecord], keyword: str = "", category: str = "", status: str = "") -> List[ItemRecord]:
    results = records
    if keyword:
        kw = keyword.lower()
        results = [r for r in results if kw in r.item_name.lower() or kw in r.description.lower() or kw in r.location.lower()]
    if category:
        results = [r for r in results if r.category.lower() == category.lower()]
    if status:
        results = [r for r in results if r.status.upper() == status.upper()]
    return results

def mark_as_claimed(records: List[ItemRecord], record_id: str) -> bool:
    for r in records:
        if r.record_id.upper() == record_id.upper() and r.status == "OPEN":
            r.status = "CLAIMED"
            r.date_claimed = datetime.now().strftime("%Y-%m-%d")
            return True
    return False

def compute_summary(records: List[ItemRecord]) -> Dict:
    total = len(records)
    lost_count = sum(1 for r in records if r.record_type == "LOST")
    found_count = sum(1 for r in records if r.record_type == "FOUND")
    claimed_count = sum(1 for r in records if r.status == "CLAIMED")
    claim_rate = (claimed_count / total * 100) if total > 0 else 0.0

    category_counts = Counter(r.category for r in records)
    location_counts = Counter(r.location for r in records)

    return {
        "total": total,
        "lost": lost_count,
        "found": found_count,
        "claimed": claimed_count,
        "open": total - claimed_count,
        "claim_rate": round(claim_rate, 1),
        "by_category": dict(category_counts),
        "top_locations": location_counts.most_common(3),
    }