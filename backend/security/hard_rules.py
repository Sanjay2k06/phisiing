import re
from typing import Tuple

def apply_hard_rules(text: str, current_score: float) -> Tuple[float, str | None]:
    """
    Absolute security overrides.
    If triggered → verdict MUST be phishing.
    """

    t = text.lower()

    # 🔥 ACCOUNT SUSPENSION + URGENCY + VERIFY (YOUR FAILURE CASE)
    if (
        re.search(r"(account|profile|security)", t)
        and re.search(r"(suspend|suspension|locked|risk|compromised)", t)
        and re.search(r"(verify|verification|credentials|immediately|urgent)", t)
    ):
        return 90.0, "Account suspension phishing pattern"

    # 🔥 OTP / PASSWORD HARVEST
    if re.search(r"(otp|one time password|password|cvv|pin)", t):
        return max(current_score, 85.0), "Credential harvesting detected"

    # 🔥 PAYMENT / MONEY DEMAND
    if re.search(r"(pay|payment|transfer|bitcoin|crypto|fee)", t):
        return max(current_score, 80.0), "Financial scam detected"

    # 🔒 No hard rule triggered
    return current_score, None
