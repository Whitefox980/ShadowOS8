import os, json
from glob import glob
from datetime import datetime
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("[!] OPENAI_API_KEY nije postavljen.")
    exit()

client = OpenAI(api_key=api_key)

logs = sorted(glob("reports/launcher_ai_*.json"), key=os.path.getmtime, reverse=True)
if not logs:
    print("[!] Nema AI launcher logova.")
    exit()

with open(logs[0]) as f:
    data = json.load(f)

top = sorted(data, key=lambda x: x.get("length", 0), reverse=True)[:5]
summary = "\n".join([f"- {x['payload']} | status: {x['status_code']} | mode: {x['mode']}" for x in top])

prompt = f"""
Evo izlaza iz AI fuzzing testa:

{summary}

Na osnovu toga:
1. Predloži kako bi backend developer trebao da zakrpi aplikaciju
2. Koje tehnologije i metode bi sprečile ove napade
3. Napiši preporuke u formi tehničkog AI bezbednosnog izveštaja

Odgovori kao White Shadow Advisor — defanzivni strateg bezbednosti.
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.4
)

content = response.choices[0].message.content
print("\n[WHITE SHADOW ADVISOR REPORT]\n")
print(content)

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out = f"reports/white_advisor_{ts}.txt"
with open(out, "w") as f:
    f.write(content)

print(f"\n[✓] Sačuvano kao: {out}")
