import shutil
import socket
from pathlib import Path
from openai import OpenAI
import json, os
from glob import glob
import subprocess
from datetime import datetime

def run_replay_commander():
    from glob import glob
    from urllib.parse import urlencode
    import json, os, requests
    from pathlib import Path
    from datetime import datetime

    try:
        log_files = sorted(glob("logs/*.json"), key=os.path.getmtime, reverse=True)
        if not log_files:
            print("[!] Nema dostupnih log fajlova.")
            return

        with open(log_files[0]) as f:
            all_payloads = json.load(f)

        hits = [p for p in all_payloads if p.get("score", 0) >= 60]
        if not hits:
            print("[•] Nema payload-a sa score ≥ 60 za replay.")
            return

        with open("config.json") as f:
            config = json.load(f)
        target = config["target_url"]

        print(f"\n[REPLAY KOMANDANT] Meta: {target} | HIT-ova: {len(hits)}\n")
        results = []

        for idx, p in enumerate(hits, 1):
            payload = p["payload"]
            category = p.get("category", "Generic")
            try:
                url = f"{target}?{urlencode({'q': payload})}"
                r = requests.get(url, timeout=5)
                print(f"[{idx}] {payload[:40]}... → {r.status_code} ({len(r.text)}B)")
                results.append({
                    "payload": payload,
                    "category": category,
                    "status_code": r.status_code,
                    "length": len(r.text)
                })
            except Exception as e:
                print(f"[{idx}] ERROR → {e}")
                results.append({"payload": payload, "error": str(e)})

        Path("reports").mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = f"reports/replay_{ts}.json"
        with open(out, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n[✓] Replay završen. Sačuvano u: {out}")

    except Exception as e:
        print(f"[!] GREŠKA tokom replay-a: {e}")
print("\n[SHADOWFOX AUTO-MODE] Pokrećem celu misiju...\n")

def run_step(name, cmd):
    print(f"\n[●] {name}...\n")
    subprocess.run(cmd, shell=True)

run_step("Mutacija i scoring", "python3 main/runner.py")
run_step("Launcher napad", "python3 main/launcher_ai.py")
run_step("Dashboard statistika", "python3 tools/shadow_dashboard.py")
# Bonus (ako želiš)
report_now = input("\nŽeliš PDF izveštaj? [y/N]: ").strip().lower()
if report_now == "y":
    run_step("PDF Report", "python3 tools/shadow_reporter.py")

advisor_now = input("\nŽeliš AI savet? [y/N]: ").strip().lower()
if advisor_now == "y":
    run_step("AI Advisor", "python3 tools/ai_advisor.py")
black_now = input("\nŽeliš crnog savetnika? [y/N]: ").strip().lower()
if black_now == "y":
    run_black_advisor()

print(f"\n[✓] Završeno. ShadowFox AutoMode kompletiran: {datetime.now().strftime('%H:%M:%S')}.\n")

run_step("Mutacija i scoring", "python3 main/runner.py")
replay_now = input("Želiš Replay?").strip().lower()
if replay_now == "y":
    run_replay_commander()
print("[SHADOWFOX AUTO-MODE] Pokrećem celu misiju ...\n")
import shutil
from datetime import datetime
from pathlib import Path


# Aktiviraj na kraju auto_mode
def find_free_port(start=8080):
    port = start
    while port < 9000:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1
    return None

def launch_frontgate():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    mission_dir = Path(f"missions/mission_{ts}")
    mission_dir.mkdir(parents=True, exist_ok=True)

    files_to_copy = [
        "output/config_launcher.json",
        "reports/pie_chart.png",
        "reports/radar_chart.png",
        "reports/*.pdf",
        "logs/*.json"
    ]

    for pattern in files_to_copy:
        for f in Path(".").glob(pattern):
            shutil.copy(f, mission_dir)

    print(f"\n[✓] Misija spakovana: {mission_dir}")

    port = find_free_port()
    if not port:
        print("[!] Nema slobodnih portova za FrontGate.")
        return

    print(f"[→] Pokrećem lokalni browser FrontGate na portu {port}...\n")
    os.chdir("missions")
    os.system(f"python3 -m http.server {port}")
launch_frontgate()

def run_black_advisor():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[!] OPENAI_API_KEY nije postavljen.")
        return

    client = OpenAI(api_key=api_key)

    logs = sorted(glob("reports/launcher_ai_*.json"), key=os.path.getmtime, reverse=True)
    if not logs:
        print("[!] Nema AI launcher logova.")
        return

    with open(logs[0]) as f:
        data = json.load(f)

    top = sorted(data, key=lambda x: x.get("length", 0), reverse=True)[:5]
    summary = "\n".join([f"- {x['payload']} | status: {x.get('status_code', '??')} | mode: {x.get('mode', 'query')}" for x in top])

    prompt = f"""
Evo izlaza iz napada AI Launcher-a:

{summary}

Na osnovu toga:
1. Predloži strategiju kako da izvedemo sledeći napad (više faza, evasion, chaining)
2. Koji mod koristiti za jači efekat (query, header, cookie)
3. Daj primer sledeće generacije payload-a koji zaobilaze detekciju

Odgovori kao Shadow AI za ofanzivnu bezbednost, bez oklevanja, u stilu komandanta.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    content = response.choices[0].message.content
    print("\n[BLACK SHADOW ADVISOR REPORT]\n")
    print(content)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = f"reports/black_advisor_{ts}.txt"
    with open(out, "w") as f:
        f.write(content)

    print(f"\n[✓] Sačuvano kao: {out}")
