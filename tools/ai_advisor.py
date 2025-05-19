import openai
import os, json
from glob import glob
from datetime import datetime

from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("[!] Nema OPENAI_API_KEY u okruženju. Prekini.")
    exit()

client = OpenAI(api_key=api_key)

logs = sorted(glob("logs/*.json"), key=os.path.getmtime, reverse=True)
if not logs:
    print("[!] Nema log fajlova.")
    exit()

with open(logs[0]) as f:
    payloads = json.load(f)

top = sorted(payloads, key=lambda x: x.get("score", 0), reverse=True)[:10]
examples = "\n".join([f"- {x['payload']} (score: {x['score']})" for x in top])

prompt = f"""
Imam sledeće testirane payload-e sa ocenama sigurnosti:

{examples}

Na osnovu ovih rezultata, daj mi konkretne savete kako da:
1. Poboljšam detekciju
2. Generišem jače varijacije
3. Kombinujem napade u sekvence

Odgovori kao stručni AI savetnik za ofanzivnu bezbednost.
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.4
)

print("\n[AI ADVISOR - ShadowFox]\n")
print(response.choices[0].message.content)
