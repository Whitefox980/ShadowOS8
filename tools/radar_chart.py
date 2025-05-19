import json
import os
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# Učitaj najnoviji log
logs = sorted(glob("logs/*.json"), key=os.path.getmtime, reverse=True)
if not logs:
    print("[!] Nema log fajlova.")
    exit()

with open(logs[0]) as f:
    data = json.load(f)

# Grupisi po kategoriji i saberi score
cat_scores = defaultdict(list)
for x in data:
    cat = x.get("category", "Unknown")
    cat_scores[cat].append(x["score"])

labels = list(cat_scores.keys())
averages = [sum(cat_scores[c]) / len(cat_scores[c]) for c in labels]

# Radar plot
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
averages += averages[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
ax.plot(angles, averages, 'o-', linewidth=2)
ax.fill(angles, averages, alpha=0.25)

ax.set_thetagrids(np.degrees(angles[:-1]), labels)
ax.set_title("Prosečan score po tipu ranjivosti", y=1.1)
ax.grid(True)

plt.savefig("reports/radar_chart.png")
print("[✓] Radar dijagram sačuvan u: reports/radar_chart.png")
