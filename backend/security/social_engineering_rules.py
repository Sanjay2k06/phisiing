from typing import Tuple

PHISHING_PHRASES = [
    "verify your credentials",
    "verify your account",
    "account will be suspended",
    "prevent permanent suspension",
    "unusual login attempt",
    "security alert",
    "confirm your identity",
    "update your information",
    "action required immediately",
    "failure to comply",
    "temporary restriction",
    "secure verification process",
    "validate your account",
    "unauthorized access detected",
    "account at risk",
]

def social_engineering_score(text: str) -> Tuple[float, str | None]:
    """
    Escalates risk if multiple real-world phishing phrases appear.
    """

    t = text.lower()
    hits = [p for p in PHISHING_PHRASES if p in t]

    if len(hits) >= 3:
        return 95.0, f"Multiple social-engineering phrases detected: {hits}"

    if len(hits) == 2:
        return 85.0, f"Strong phishing language detected: {hits}"

    return 0.0, None
