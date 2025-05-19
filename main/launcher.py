import json, requests
from urllib.parse import urlencode
from pathlib import Path
from datetime import datetime

with open("output/config_launcher.json") as f:
    data = json.load(f)

target = data["target_url"]
payloads = data["hit_payloads"]
results = []

for p in payloads:
    payload = p["payload"]
    category = p.get("category", "Generic")
    try:
        url = f"{target}?{urlencode({'q': payload})}"
        r = requests.get(url, timeout=5)
        results.append({
            "payload": payload,
            "status_code": r.status_code,
            "length": len(r.text),
            "success": r.status_code in [200, 302],
            "category": category
        })
        print(f"[+] {payload} → {r.status_code} | {len(r.text)}B")
    except Exception as e:
        results.append({"payload": payload, "error": str(e), "category": category})
        print(f"[!] ERROR: {payload} → {e}")

Path("reports").mkdir(exist_ok=True)
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f"reports/launcher_{ts}.json", "w") as f:
    json.dump(results, f, indent=2)
