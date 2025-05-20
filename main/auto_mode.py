import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import shutil
import socket
from pathlib import Path
from openai import OpenAI
import json
from glob import glob
import subprocess
from datetime import datetime
from rich.console import Console


# Dinamički preuzmi metu
target = sys.argv[1] if len(sys.argv) > 1 else "https://geocode-beta.bykea.net"
console = Console()
auto_agentfuzz = True
def set_target_url():
    target = input("Enter target URL (e.g., https://target.com): ").strip()
    if not target.startswith("http"):
        target = "https://" + target

    with open("config.json", "w") as f:
        json.dump({"target_url": target}, f)
    print(f"[✓] Target set to: {target}")
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

def run_white_advisor():
    import subprocess
    print("\n[●] Aktiviram belog savetnika...")
    subprocess.run("python3 tools/white_shadow_advisor.py", shell=True)
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

def run_shadow_monitor():
    import subprocess
    from glob import glob
    import os
    import time
    time.sleep(2)

    files = sorted(glob("reports/launcher_ai_*.json"), key=os.path.getmtime, reverse=True)
    if not files:
        print("[!] No launcher_ai logs found.")
        return

    latest_log = files[0]
    if os.path.getsize(latest_log) < 100:
        print("[!] Log file too small, skipping ShadowMonitor.")
        return

    subprocess.run("python3 tools/shadow_monitor.py", shell=True)
def run_poc_report():
    import subprocess
    print("\n[●] Generating PoC report...")
    subprocess.run("python3 tools/poc_generator.py", shell=True)
def run_waf_analyzer():
    import subprocess
    subprocess.run("python3 tools/waf_analyzer.py", shell=True)
def set_target_url():
    target = input("Enter target URL (e.g., https://target.com): ").strip()
    with open("config.json", "w") as f:
        json.dump({"target_url": target}, f)
    print(f"[✓] Target set to: {target}")
def run_anomaly_trigger():
    import subprocess
    subprocess.run("python3 tools/anomaly_trigger.py", shell=True)
def activate_agentfuzz(target):
    from agents.agentfuzz import run_agentfuzz
    run_agentfuzz(target)

def run_shadowchain():
    import subprocess
    print("\n[●] ShadowChain sekvencijalni napad...")
    subprocess.run("python3 tools/shadow_chain.py", shell=True)
def run_step(name, cmd):
    print(f"\n[●] {name}...\n")
    subprocess.run(cmd, shell=True)
set_target_url()
run_step("Mutacija i scoring", "python3 main/runner.py")
run_step("Launcher napad", "python3 main/launcher_ai.py")
run_step("Dashboard statistika", "python3 tools/shadow_dashboard.py")


run_step("Monitoring odgovora", "python3 tools/shadow_monitor.py")
def run_xss_mutation_gen():
    import subprocess
    subprocess.run("python3 tools/xss_mutation_gen.py", shell=True)

# Pitanje korisniku:
mutation_now = input("\nDo you want to generate XSS mutation payloads? [y/N]: ").strip().lower()
if mutation_now == "y":
    run_xss_mutation_gen()
# Bonus (ako želiš)
report_now = input("\nŽeliš PDF izveštaj? [y/N]: ").strip().lower()
if report_now == "y":
    run_step("PDF Report", "python3 tools/shadow_reporter.py")

anomaly_now = input("\nDo you want to scan for anomalous payload behavior? [y/N]: ").strip().lower()
if anomaly_now == "y":
    run_anomaly_trigger()
waf_now = input("\nDo you want to analyze WAF response behavior? [y/N]: ").strip().lower()
if waf_now == "y":
    run_waf_analyzer()
advisor_now = input("\nŽeliš AI savet? [y/N]: ").strip().lower()
if advisor_now == "y":
    run_step("AI Advisor", "python3 tools/ai_advisor.py")
white_now = input("\nŽeliš belog savetnika? [y/N]: ").strip().lower()
if white_now == "y":
    run_white_advisor()
black_now = input("\nŽeliš crnog savetnika? [y/N]: ").strip().lower()
if black_now == "y":
    run_black_advisor()
chain_now = input("\nŽeliš ShadowChain tok? [y/N]: ").strip().lower()
if chain_now == "y":
    run_shadowchain()
print(f"\n[✓] Završeno. ShadowFox AutoMode kompletiran: {datetime.now().strftime('%H:%M:%S')}.\n")

run_step("Mutacija i scoring", "python3 main/runner.py")
replay_now = input("Želiš Replay?").strip().lower()
if replay_now == "y":
    run_replay_commander()
console.print("\n[●] Aktiviram ShadowRecon izviđača...", style="bold cyan")
os.system("python3 agents/agent_mapper.py")
print("[SHADOWFOX AUTO-MODE] Pokrećem celu misiju ...\n")
# === AGENT X: FINALNA FAZA ===
use_agentx = input("\nŽeliš da aktiviraš AgentX napad? [y/N]: ").strip().lower()
if use_agentx == "y":
    console.print("[●] Pokrećem AgentX završni napad...", style="bold red")
    os.system("python3 agents/agentx.py")
# === LogicFuzzer faza: test auth bypass i IDOR ===
console.print("\n[●] Pokrećem LogicFuzzer za test poslovne logike...", style="bold cyan")
os.system("python3 agents/logic_fuzzer.py")
if auto_agentfuzz:
    activate_agentfuzz(target)
poc_now = input("\nDo you want to generate a PoC report? [y/N]: ").strip().lower()
if poc_now == "y":
    run_poc_report()

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

