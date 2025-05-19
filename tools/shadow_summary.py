import json, os
from glob import glob

log_files = glob("logs/*.json")
all = []

for file in log_files:
    with open(file) as f:
        all.extend(json.load(f))

if not all:
    print("Nema podataka za analizu.")
    exit()

print(f"\n[+] Testiranih payload-a: {len(all)}")
avg_score = sum(x["score"] for x in all) / len(all)
top = sorted(all, key=lambda x: x["score"], reverse=True)[:5]

print(f"[+] Prosečan score: {avg_score:.2f}")
print("[+] Top 5 payload-a:\n")
for i, x in enumerate(top, 1):
    print(f"{i}. {x['payload']}  →  {x['score']} ({x['category']})")
