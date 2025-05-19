import requests
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()

# Učitaj metu
with open("config.json") as f:
    config = json.load(f)

target = config.get("target_url", "").strip()
if not target.startswith("http"):
    target = "https://" + target

# Primeri test ID-ova koje napadamo
test_ids = [1, 2, 3, 4, 5, 1001, 9999]

# Rute koje sadrže podatke vezane za korisnike
endpoints = [
    "/api/user?id=",
    "/api/order?id=",
    "/api/profile?id=",
    "/wallet/view?id=",
    "/booking/status?id=",
]

headers = {
    "User-Agent": "ShadowFox-LogicFuzzer",
    "X-Bug-Bounty": "h1-yourusername"
}

console.print(f"[●] Pokrećem LogicFuzzer za metu: {target}", style="bold cyan")
table = Table(title="IDOR / Logic Test Rezultati", show_lines=True)
table.add_column("URL", style="cyan")
table.add_column("Status", style="yellow")
table.add_column("Size", justify="right")

results = []

for route in endpoints:
    for test_id in test_ids:
        url = f"{target}{route}{test_id}"
        try:
            r = requests.get(url, headers=headers, timeout=5)
            size = len(r.content)
            table.add_row(url, str(r.status_code), str(size))
            results.append({
                "url": url,
                "status": r.status_code,
                "length": size,
                "reflected": str(test_id) in r.text
            })
        except Exception as e:
            console.print(f"[!] Greška za {url}: {e}", style="red")

console.print(table)

# Sačuvaj
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f"reports/logicfuzzer_{ts}.json", "w") as f:
    json.dump(results, f, indent=2)

console.print(f"\n[✓] Rezultati sačuvani: reports/logicfuzzer_{ts}.json", style="green")
