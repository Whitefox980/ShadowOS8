import os, sys, json
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mutation.smart_mutator import SmartMutator

def main():
    with open("config.json") as f:
        config = json.load(f)

    target = config["target_url"]
    mode = config.get("mode", "normal")
    count = config.get("payload_count", 10)
    fallback = config.get("enable_fallback", True)

    mutator = SmartMutator(target_url=target)
    results = mutator.generate_payloads(count=count, mode=mode)
    mutator.log_session()

    hit_payloads = [r for r in results if r["score"] >= 60]

    if not hit_payloads and fallback:
        print("[!] Fallback aktiviran: pokrećem agresivni mod...")
        results = mutator.generate_payloads(count=10, mode="aggressive")
        mutator.log_session()
        hit_payloads = [r for r in results if r["score"] >= 60]

    Path("output").mkdir(exist_ok=True)
    with open("output/config_launcher.json", "w") as f:
        json.dump({
            "target_url": target,
            "hit_payloads": hit_payloads
        }, f, indent=2)

    print(f"\n[✓] HIT payloada: {len(hit_payloads)} spremljeno za launcher.")

if __name__ == "__main__":
    main()
