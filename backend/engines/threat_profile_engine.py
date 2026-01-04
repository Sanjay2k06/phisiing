# backend/engines/threat_profile_engine.py

class ThreatProfileEngine:
    """
    Builds a psychological and impact-based threat profile.
    """

    def analyze(self, content: str):
        text = content.lower()

        manipulation = []
        impact = {
            "financial_loss": False,
            "credential_compromise": False,
            "emotional_distress": False
        }

        # Manipulation techniques
        if any(w in text for w in ["urgent", "act now", "limited time"]):
            manipulation.append("Urgency Pressure")
            impact["emotional_distress"] = True

        if any(w in text for w in ["won", "congratulations", "reward", "prize"]):
            manipulation.append("Reward Exploitation")

        if any(w in text for w in ["bank", "support team", "security team"]):
            manipulation.append("Authority Impersonation")

        # Impact analysis
        if any(w in text for w in ["fee", "payment", "transfer"]):
            impact["financial_loss"] = True

        if any(w in text for w in ["password", "otp", "verify account"]):
            impact["credential_compromise"] = True

        return {
            "manipulation_techniques": manipulation,
            "potential_impact": impact
        }
