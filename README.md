# Campus Lost-and-Found Register (CLI)

A modular, crash-proof Python command-line application built to modernize campus lost-and-found management. Designed for speed, data integrity, and actionable administrative insights, it replaces manual paper registers with automated match detection, defensive input validation, dual JSON/CSV persistence, and visual executive reporting.

---

## Key Features
* **Smart Match Detection:** Automatically cross-references newly logged `LOST` and `FOUND` records using weighted scoring across category, item-name keywords, and campus location to alert users immediately.
* **Defensive Input Validation:** Prevents runtime crashes by enforcing non-empty text, valid calendar dates (blocking future dates), strict category selections, and regex-validated email addresses or 10-digit phone numbers.
* **Dual Persistence & Recovery:** Automatically saves records to `records.json` (with built-in recovery if the file is missing or corrupted) and supports one-click CSV export and row-validated bulk CSV import.
* **Overdue Item Alerts:** Automatically flags `OPEN` records older than 14 days with yellow ANSI `[OVERDUE]` highlights in the terminal register.
* **Executive Analytics & Reporting:** Computes recovery rates, average resolution time in days, and campus hotspots, exporting both a 3-panel Matplotlib chart (`campus_summary_charts.png`) and a formatted Markdown report (`campus_report.md`).

---

## Project Architecture

```text
├── main.py                      # Terminal UI, menu loop, ANSI alerts, and Markdown report export
├── models.py                    # ItemRecord dataclass, category definitions, and serialization
├── storage.py                   # Crash-safe JSON persistence, CSV export, and row-validated CSV import
├── validators.py                # Input sanitization, date checks, and email/phone regex validation
├── engine.py                    # Weighted match scoring, search/filtering, claim updates, and analytics
├── visualizer.py                # 3-panel Matplotlib chart generator (Category, Status, Campus Hotspots)
├── records.json                 # Persistent dataset (seeded with 35 realistic campus records)
├── requirements.txt             # Locked Python dependencies
└── campus_summary_charts.png    # Auto-generated visual analytics dashboard