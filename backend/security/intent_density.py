import re
from typing import Tuple

AUTHORITY = ["bank", "security team", "administrator", "support", "service"]
URGENCY = ["immediately", "urgent", "now", "within 24 hours", "today"]
THREAT = ["suspend", "terminate", "lock", "disable", "restrict"]

def intent_density_score(text: str) -> Tuple[float, str | None]:
    t = text.lower()

    authority = sum(1 for w in AUTHORITY if w in t)
    urgency = sum(1 for w in URGENCY if w in t)
    threat = sum(1 for w in THREAT if w in t)

    score = authority + urgency + threat

    if score >= 4:
        return 90.0, "High intent-density phishing signal"

    if score == 3:
        return 80.0, "Moderate intent-density phishing signal"

    return 0.0, None
