import requests
import json
import os
from datetime import datetime
from urllib.parse import quote
from glob import glob
from rich.console import Console
from rich.table import Table

console = Console()

# Učitaj metu
with open("config.json") as f:
    config = json.load(f)

target = config.get("target_url", "").strip()
if not target.startswith("http"):
    target = "https://" + target

# Učitaj payload-e
latest_mutation = sorted(glob("logs/xss_mutations_*.json"), key=os.path.getmtime)[-1]
with open(latest_mutation) as f:
    selected_payloads = json.load(f)[:25]  # limit za brže testiranje

# Učitaj reflektovane parametre od ShadowRecon izviđača
try:
    latest_reflect = sorted(glob("logs/reflected_params_*.json"), key=os.path.getmtime)[-1]
    with open(latest_reflect) as f:
        reflected_params = json.load(f)
except:
    reflected_params = ["q"]  # fallback

console.print(f"\n[✓] Detektovani reflektovani parametri: {reflected_params}", style="bold cyan")
console.print(f"[●] AgentX Selected Payloads\n", style="bold green")

# Prikaz payload-a
table = Table(show_header=True, header_style="bold magenta")
table.add_column("Score", width=6)
table.add_column("Payload")

for p in selected_payloads:
    table.add_row(str(30), p[:100])

console.print(table)

# Testiranje
console.print("\n[-] Izvršavam napade …", style="bold yellow")
results = []

for param in reflected_params:
    for idx, payload in enumerate(selected_payloads, 1):
        try:
            full_url = f"{target}?{param}={quote(payload)}"
            r = requests.get(full_url, timeout=5)

            reflected = payload in r.text
            console.print(
                f"[+] {param}=... ➜ {r.status_code} | size={len(r.content)} | reflect={reflected}",
                style="green" if reflected else "grey50"
            )

            results.append({
                "param": param,
                "payload": payload,
                "status_code": r.status_code,
                "length": len(r.content),
                "reflect": reflected
            })

        except Exception as e:
            console.print(f"[!] Greška za {param}: {e}", style="red")

# Sačuvaj
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out_path = f"reports/agentx_result_{ts}.json"
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)

console.print(f"\n[x] AgentX napad završen. Izveštaj sačuvan u: {out_path}", style="bold green")
