# engine.py
from collections import Counter
from datetime import datetime
from typing import List, Dict
from models import ItemRecord

def generate_next_id(records: List[ItemRecord], record_type: str) -> str:
    prefix = "LST" if record_type == "LOST" else "FND"
    return f"{prefix}-{len(records) + 1:04d}"

def find_potential_matches(new_item: ItemRecord, records: List[ItemRecord]) -> List[ItemRecord]:
    """Scores and ranks opposite-type OPEN records by category, keyword, and location overlap."""
    target_type = "FOUND" if new_item.record_type == "LOST" else "LOST"
    new_words = set(new_item.item_name.lower().split())
    scored_matches = []

    for r in records:
        if r.record_type == target_type and r.status == "OPEN":
            score = 0
            if r.category == new_item.category:
                score += 2
            existing_words = set(r.item_name.lower().split())
            score += len(new_words & existing_words) * 3
            if r.location.lower() == new_item.location.lower():
                score += 2
            if score >= 4:
                scored_matches.append((score, r))

    scored_matches.sort(key=lambda pair: pair[0], reverse=True)
    return [r for _, r in scored_matches]

def is_overdue(record: ItemRecord, days: int = 14) -> bool:
    if record.status != "OPEN":
        return False
    reported = datetime.strptime(record.date_reported, "%Y-%m-%d").date()
    return (datetime.now().date() - reported).days > days

def get_overdue_records(records: List[ItemRecord], days: int = 14) -> List[ItemRecord]:
    return [r for r in records if is_overdue(r, days)]

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
    claimed_records = [r for r in records if r.status == "CLAIMED"]
    claimed_count = len(claimed_records)
    claim_rate = (claimed_count / total * 100) if total > 0 else 0.0

    # Average days to claim
    resolution_days = []
    for r in claimed_records:
        if r.date_claimed:
            d1 = datetime.strptime(r.date_reported, "%Y-%m-%d").date()
            d2 = datetime.strptime(r.date_claimed, "%Y-%m-%d").date()
            resolution_days.append(max(0, (d2 - d1).days))
    avg_days = round(sum(resolution_days) / len(resolution_days), 1) if resolution_days else 0.0

    return {
        "total": total,
        "lost": lost_count,
        "found": found_count,
        "claimed": claimed_count,
        "open": total - claimed_count,
        "overdue": len(get_overdue_records(records)),
        "claim_rate": round(claim_rate, 1),
        "avg_resolution_days": avg_days,
        "by_category": dict(Counter(r.category for r in records)),
        "by_location": dict(Counter(r.location for r in records).most_common(5)),
        "top_locations": Counter(r.location for r in records).most_common(3),
    }