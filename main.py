from models import ItemRecord, CATEGORIES, RECORD_TYPES
from storage import load_records, save_records
from validators import get_non_empty_string, get_choice, get_valid_date, get_valid_contact
from engine import generate_next_id, find_potential_matches, search_records, mark_as_claimed, compute_summary
from visualizer import generate_charts

def print_table(records: list[ItemRecord]) -> None:
    if not records:
        print("\n  No matching records found.")
        return
    header = f"{'ID':<10} | {'TYPE':<6} | {'ITEM NAME':<20} | {'CATEGORY':<22} | {'LOCATION':<15} | {'DATE':<10} | {'STATUS':<7}"
    print("\n" + "-" * len(header))
    print(header)
    print("-" * len(header))
    for r in records:
        print(f"{r.record_id:<10} | {r.record_type:<6} | {r.item_name[:20]:<20} | {r.category[:22]:<22} | {r.location[:15]:<15} | {r.date_reported:<10} | {r.status:<7}")
    print("-" * len(header))

def handle_add_record(records: list[ItemRecord]) -> None:
    print("\n--- Log New Lost / Found Item ---")
    rec_type = get_choice("Record Type: ", RECORD_TYPES)
    name = get_non_empty_string("Item Name: ")
    category = get_choice("Category: ", CATEGORIES)
    location = get_non_empty_string("Campus Location: ")
    date_str = get_valid_date()
    desc = input("Description (optional): ").strip()
    contact = get_valid_contact()

    new_id = generate_next_id(records, rec_type)
    new_record = ItemRecord(new_id, rec_type, name, category, location, date_str, desc, contact)
    records.append(new_record)
    save_records(records)
    print(f"\n[Success] Logged record {new_id}!")

    matches = find_potential_matches(new_record, records[:-1])
    if matches:
        print(f"\n[!] ALERT: Found {len(matches)} potential match(es) in existing records:")
        print_table(matches)

def main() -> None:
    records = load_records()
    while True:
        print("\n==========================================")
        print("   CAMPUS LOST-AND-FOUND REGISTER (CLI)   ")
        print("==========================================")
        print("1. Log Lost or Found Item")
        print("2. View All Records")
        print("3. Search / Filter Records")
        print("4. Mark Item as Claimed")
        print("5. Executive Summary & Export Charts")
        print("6. Exit")

        choice = input("\nSelect an option (1-6): ").strip()

        if choice == "1":
            handle_add_record(records)
        elif choice == "2":
            print_table(records)
        elif choice == "3":
            kw = input("Keyword (leave blank for all): ").strip()
            status = input("Status filter (OPEN/CLAIMED or blank): ").strip()
            print_table(search_records(records, keyword=kw, status=status))
        elif choice == "4":
            rec_id = input("Enter Record ID to mark CLAIMED (e.g., LST-0001): ").strip()
            if mark_as_claimed(records, rec_id):
                save_records(records)
                print(f"[Success] Record {rec_id.upper()} updated to CLAIMED.")
            else:
                print("[!] Record not found or already claimed.")
        elif choice == "5":
            summary = compute_summary(records)
            print("\n--- Executive Summary ---")
            print(f"Total Records : {summary['total']} (Lost: {summary['lost']} | Found: {summary['found']})")
            print(f"Status        : Open: {summary['open']} | Claimed: {summary['claimed']} ({summary['claim_rate']}% recovery)")
            print(f"Top Hotspots  : {summary['top_locations']}")
            if generate_charts(summary):
                print("[Success] Visual report saved to 'campus_summary_charts.png'.")
        elif choice == "6":
            print("Saving state and exiting. Goodbye!")
            break
        else:
            print("[!] Invalid choice. Enter a number from 1 to 6.")

if __name__ == "__main__":
    main()