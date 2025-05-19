
import os
import time
import json
from glob import glob
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from pathlib import Path

console = Console()
ts = datetime.now().strftime("%Y%m%d_%H%M%S")

# Nađi najnoviji launcher rezultat

files = sorted(glob("reports/launcher_ai_*.json"), key=os.path.getmtime, reverse=True)
if not files:
    console.print("[!] No launcher_ai_* files found in reports/", style="bold red")
    exit()

with open(files[0]) as f:
    data = json.load(f)

status_count = {"200": 0, "403": 0, "500": 0, "other": 0}
total = len(data)

table = Table(title=f"ShadowMonitor [{total} Payloads] - {ts}", style="bold white")
table.add_column("Index", justify="right")
table.add_column("Status", justify="center")
table.add_column("Size", justify="right")
table.add_column("Payload (trimmed)", style="cyan")

with Live(table, refresh_per_second=6):
    for idx, d in enumerate(data, 1):
        status = str(d.get("status_code", "??"))
        size = str(d.get("length", "-"))
        payload = d.get("payload", "")[:40] + "..."

        # Statistika
        if status == "200":
            status_count["200"] += 1
        elif status == "403":
            status_count["403"] += 1
        elif status == "500":
            status_count["500"] += 1
        else:
            status_count["other"] += 1

        color = "green" if status == "200" else "red" if status == "403" else "yellow" if status == "500" else "grey"
        table.add_row(str(idx), f"[{color}]{status}[/{color}]", size, payload)
        time.sleep(0.15)

# Finalni rezime
console.print("\n[✓] ShadowMonitor completed.\n", style="bold green")
console.print(f"Total payloads: {total}")
for k, v in status_count.items():
    console.print(f"- {k}: {v}")
