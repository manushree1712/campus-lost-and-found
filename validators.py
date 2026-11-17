import re
from datetime import datetime
from typing import List

def get_non_empty_string(prompt: str, min_len: int = 2) -> str:
    while True:
        val = input(prompt).strip()
        if len(val) >= min_len:
            return val
        print(f"  [!] Input must be at least {min_len} characters long.")

def get_choice(prompt: str, options: List[str]) -> str:
    options_upper = [opt.upper() for opt in options]
    while True:
        print(f"  Options: {', '.join(options)}")
        val = input(prompt).strip()
        if val.upper() in options_upper:
            return options[options_upper.index(val.upper())]
        print("  [!] Invalid selection. Please choose from the listed options.")

def get_valid_date(prompt: str = "Date (YYYY-MM-DD): ") -> str:
    while True:
        val = input(prompt).strip()
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return val
        except ValueError:
            print("  [!] Invalid date format. Use YYYY-MM-DD (e.g., 2026-11-17).")

def get_valid_contact(prompt: str = "Contact (Email or 10-digit phone): ") -> str:
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    phone_pattern = r"^\d{10}$"
    while True:
        val = input(prompt).strip()
        if re.match(email_pattern, val) or re.match(phone_pattern, val):
            return val
        print("  [!] Enter a valid email address or 10-digit phone number.")