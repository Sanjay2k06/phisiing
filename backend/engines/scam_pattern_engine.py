from typing import Dict, List


class ScamPatternEngine:
    """
    Senior Scam Pattern Engine
    Detects real-world scam workflows using
    stage-based and intent-aware logic.
    """

    def __init__(self):
        self.scam_workflows = {
            "delivery_scam": {
                "stages": [
                    ["delivery", "package", "parcel"],
                    ["failed", "pending", "held"],
                    ["confirm", "verify", "link"]
                ],
                "base_score": 30,
                "message": "Delivery scam workflow detected"
            },
            "otp_scam": {
                "stages": [
                    ["otp", "verification code", "one time password"],
                    ["share", "enter", "send"]
                ],
                "base_score": 40,
                "message": "OTP credential theft workflow detected"
            },
            "prize_scam": {
                "stages": [
                    ["congratulations", "winner", "won"],
                    ["prize", "reward", "gift"],
                    ["claim", "collect"]
                ],
                "base_score": 35,
                "message": "Prize or lottery scam workflow detected"
            },
            "account_takeover": {
                "stages": [
                    ["account", "login", "access"],
                    ["suspended", "locked", "restricted"],
                    ["verify", "update", "confirm"]
                ],
                "base_score": 40,
                "message": "Account takeover phishing workflow detected"
            },
            "payment_trap": {
                "stages": [
                    ["payment", "transaction", "billing"],
                    ["failed", "error", "declined"],
                    ["update", "verify"]
                ],
                "base_score": 32,
                "message": "Payment failure trap detected"
            },
            "job_fraud": {
                "stages": [
                    ["job", "work", "employment"],
                    ["selected", "hired", "offer"],
                    ["fee", "registration", "payment"]
                ],
                "base_score": 30,
                "message": "Job fraud workflow detected"
            }
        }

        self.money_signals = [
            "pay", "send", "transfer", "wire",
            "$", "usd", "inr", "crypto", "bitcoin"
        ]

        self.credential_signals = [
            "password", "otp", "pin", "cvv",
            "card number", "aadhar", "pan"
        ]

    # ---------------- MAIN ENTRY ----------------
    async def analyze(self, content: str, mode: str) -> Dict:
        text = content.lower()
        findings = []
        timeline = []     # ✅ STEP-3
        risk_score = 0
        detected_workflows = []

        # 🚨 HARD PHISHING RULE
        if (
            ("account" in text or "profile" in text)
            and ("suspend" in text or "restricted" in text or "locked" in text)
            and ("verify" in text or "confirm" in text or "immediately" in text)
        ):
            risk_score += 45
            findings.append(
                "Critical phishing pattern: Account suspension threat with urgency"
            )
            timeline.append("Account suspension + urgency detected (+45)")

        # ---- Workflow Detection ----
        for name, data in self.scam_workflows.items():
            if self._workflow_matched(text, data["stages"]):
                detected_workflows.append(name)
                risk_score += data["base_score"]
                findings.append(data["message"])
                timeline.append(f"{data['message']} (+{data['base_score']})")

        # ---- Escalation Rules ----
        if len(detected_workflows) >= 2:
            risk_score += 25
            findings.append(
                f"Multiple scam workflows detected: {', '.join(detected_workflows)}"
            )
            timeline.append("Multiple scam workflows escalated (+25)")

        # ---- Money Extraction ----
        if any(sig in text for sig in self.money_signals):
            risk_score += 25
            findings.append("Financial extraction attempt detected")
            timeline.append("Financial extraction signal (+25)")

        # ---- Credential Theft ----
        if any(sig in text for sig in self.credential_signals):
            risk_score += 35
            findings.append("Credential harvesting attempt detected")
            timeline.append("Credential harvesting signal (+35)")

        # ---- Trust Floor ----
        if risk_score > 0 and risk_score < 30:
            risk_score = 30
            findings.append("Scam trust floor applied")
            timeline.append("Trust floor applied (min 30)")

        return {
            "engine_name": "Scam Pattern Engine (Senior)",
            "risk_score": min(risk_score, 100),
            "findings": findings,
            "confidence": 0.95 if findings else 0.4,
            "timeline": timeline   # ✅ STEP-3
        }

    # ---------------- WORKFLOW MATCH ----------------
    def _workflow_matched(self, text: str, stages: List[List[str]]) -> bool:
        index = 0
        words = text.split()

        for stage in stages:
            found = False
            for i in range(index, len(words)):
                if any(keyword in words[i] for keyword in stage):
                    index = i + 1
                    found = True
                    break
            if not found:
                return False

        return True
