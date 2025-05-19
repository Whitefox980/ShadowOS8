import json, os
from datetime import datetime

HIST_FILE = "scoring/adaptive_score.jsonl"

def score_payload(payload, category):
    score = 0
    if "<script>" in payload: score += 25
    if "'" in payload or "--" in payload: score += 20
    if "union" in payload.lower(): score += 15
    ai_bonus = min(payload.count("=") * 5, 20)
    score += ai_bonus

    result = {
        "payload": payload,
        "score": score,
        "category": category,
        "timestamp": datetime.now().isoformat(),
        "hit": score >= get_threshold(category)
    }

    with open(HIST_FILE, "a") as f:
        f.write(json.dumps(result) + "\n")

    return result

def get_threshold(category):
    try:
        with open(HIST_FILE) as f:
            scores = [json.loads(l)["score"] for l in f if json.loads(l)["category"] == category]
        if not scores:
            return 40  # fiksni fallback prag ako nema istorije
        return int(sum(scores) / len(scores) * 0.7)  # lakši prolaz
    except:
        return 40
