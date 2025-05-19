import json
import requests
from urllib.parse import urlencode
from datetime import datetime
from pathlib import Path
from glob import glob

# Učitaj najnoviji log sa payloadima i score-ovima
log_files = sorted(glob("logs/*.json"), key=os.path.getmtime, reverse=True)
if not log_files:
    print("[!] Nema dostupnih log fajlova.")
    exit()

with open(log_files[0]) as f:
    all_payloads = json.load(f)

# Filteruj HIT-ove
hits = [p for p in all_payloads if p.get("score", 0) >= 60]
if not hits:
    print("[•] Nema payload-a sa score ≥ 60 za replay.")
    exit()

# Učitaj metu iz config fajla
with open("config.json") as f:
    config = json.load(f)
target = config["target_url"]

# Replay svaki HIT payload
print(f"\n[REPLAY KOMANDANT] Meta: {target} | Payloada: {len(hits)}\n")
results = []

for idx, p in enumerate(hits, 1):
    payload = p["payload"]
    category = p.get("category", "Generic")
    try:
        url = f"{target}?{urlencode({'q': payload})}"
        r = requests.get(url, timeout=5)
        print(f"[{idx}] {payload[:40]}... → {r.status_code} ({len(r.text)}B)")
        results.append({
            "payload": payload,
            "category": category,
            "status_code": r.status_code,
            "length": len(r.text)
        })
    except Exception as e:
        print(f"[{idx}] ERROR → {e}")
        results.append({"payload": payload, "error": str(e)})

# Sačuvaj rezultate
Path("reports").mkdir(exist_ok=True)
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out_file = f"reports/replay_{ts}.json"

with open(out_file, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n[✓] Replay završen. Rezultati sačuvani u: {out_file}")
