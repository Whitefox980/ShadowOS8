import json
import requests
from urllib.parse import urlencode
from pathlib import Path
from datetime import datetime

def smart_inject(url, payload, mode="query"):
    try:
        if mode == "query":
            full_url = f"{url}?{urlencode({'q': payload})}"
            r = requests.get(full_url, timeout=5)
        elif mode == "header":
            r = requests.get(url, headers={"X-Fuzz": payload}, timeout=5)
        elif mode == "cookie":
            r = requests.get(url, cookies={"session": payload}, timeout=5)
        else:
            r = requests.get(url, timeout=5)
        return r
    except Exception as e:
        return e

# Učitavanje payload-a iz output fajla
with open("output/config_launcher.json") as f:
    config = json.load(f)

target = config["target_url"]
payloads = config["hit_payloads"]
results = []

print(f"\n[AI LAUNCHER] Meta: {target}")
for idx, p in enumerate(payloads, 1):
    pl = p["payload"]
    category = p.get("category", "Generic")

    mode = "query"
    if "XSS" in category and "<" in pl:
        mode = "header" if random.choice([True, False]) else "cookie"
    if "SQL" in category:
        mode = "query"

    response = smart_inject(target, pl, mode)

    if isinstance(response, Exception):
        print(f"[{idx}] ERROR → {pl} | {response}")
        results.append({"payload": pl, "error": str(response), "category": category})
    else:
        print(f"[{idx}] {mode.upper()} | {pl[:40]}... → {response.status_code} ({len(response.text)}B)")
        results.append({
            "payload": pl,
            "mode": mode,
            "status_code": response.status_code,
            "length": len(response.text),
            "category": category
        })

# Snimi rezultat
Path("reports").mkdir(exist_ok=True)
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out = f"reports/launcher_ai_{ts}.json"
with open(out, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n[✓] AI Launcher završen. Rezultat u: {out}")
