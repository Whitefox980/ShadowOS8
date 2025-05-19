import json, os
from glob import glob
from pathlib import Path

BANK_FILE = "bank/payload_bank.jsonl"

def load_bank():
    if not os.path.exists(BANK_FILE):
        return set()
    with open(BANK_FILE) as f:
        return set(line.strip() for line in f)

def save_to_bank(payloads):
    with open(BANK_FILE, "a") as f:
        for p in payloads:
            f.write(p.strip() + "\n")

# Učitaj sve log fajlove
logs = sorted(glob("logs/*.json"))
all_payloads = []

for log in logs:
    with open(log) as f:
        data = json.load(f)
        all_payloads.extend([x["payload"] for x in data if x.get("score", 0) >= 40])

# Ukloni duplikate
existing = load_bank()
new_unique = [p for p in all_payloads if p not in existing]

# Sačuvaj
if new_unique:
    save_to_bank(new_unique)
    print(f"[✓] Dodato u banku: {len(new_unique)} payload-a.")
else:
    print("[•] Nema novih payload-a za dodavanje.")
