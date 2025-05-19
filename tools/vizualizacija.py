import json
import os
from glob import glob
from collections import Counter
import matplotlib.pyplot as plt

# Učitaj poslednji log
logs = sorted(glob("logs/*.json"), key=os.path.getmtime, reverse=True)
if not logs:
    print("[!] Nema dostupnih log fajlova.")
    exit()

with open(logs[0]) as f:
    data = json.load(f)

# Grupisi po kategoriji
categories = [x.get("category", "Unknown") for x in data]
counts = Counter(categories)

# Prikaži kao pie chart
labels = list(counts.keys())
sizes = list(counts.values())

plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.axis("equal")
plt.title("Distribucija Payload Kategorija (Heatmapa)")
plt.savefig("reports/pie_chart.png")
print("[✓] Pie chart sačuvan u: reports/pie_chart.png")
