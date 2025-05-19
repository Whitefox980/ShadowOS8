import requests
from urllib.parse import urlencode
from rich.console import Console
from rich.table import Table
import json
from datetime import datetime

console = Console()

# Učitaj metu
with open("config.json") as f:
    config = json.load(f)

target = config.get("target_url", "").strip()
if not target.startswith("http"):
    target = "https://" + target

params_to_test = [
    "q", "search", "term", "input", "id", "query", "name", "message", "email", "data"
]

reflected = []

console.print(f"[●] ShadowRecon: Testiram reflektujuće parametre za {target}\n", style="bold cyan")

for param in params_to_test:
    test_value = "XSS123TEST"
    url = f"{target}?{urlencode({param: test_value})}"
    try:
        r = requests.get(url, timeout=6)
        if test_value in r.text:
            console.print(f"[✓] Reflektovan parametar: {param}", style="green")
            reflected.append(param)
        else:
            console.print(f"[×] Nije reflektovan: {param}", style="grey50")
    except Exception as e:
        console.print(f"[!] Greška za {param}: {e}", style="red")

# Sačuvaj
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out = f"logs/reflected_params_{ts}.json"
with open(out, "w") as f:
    json.dump(reflected, f, indent=2)

console.print(f"\n[✓] Reflektujući parametri sačuvani u: {out}", style="bold green")
