"""
SAFE Machine Learning Engine
NO pickle
NO training
NO crashes
ML is SUPPORT ONLY
"""

from typing import Dict
import math

class MLDetectionEngine:
    """
    ML-style probabilistic scoring using heuristics.
    Designed to NEVER override security rules.
    """

    async def analyze(self, content: str, mode: str) -> Dict:
        text = content.lower()

        score = 0
        findings = []

        # Heuristic ML-like signals
        if any(x in text for x in ["verify", "confirm", "update", "secure"]):
            score += 15
            findings.append("ML heuristic: action request detected")

        if any(x in text for x in ["urgent", "immediately", "within 24 hours"]):
            score += 15
            findings.append("ML heuristic: urgency detected")

        if any(x in text for x in ["account", "suspended", "locked"]):
            score += 20
            findings.append("ML heuristic: account threat language")

        if "http" in text or "www." in text:
            score += 10
            findings.append("ML heuristic: link present")

        # ML can NEVER exceed 40
        score = min(score, 40)

        return {
            "engine_name": "Machine Learning Engine (Safe)",
            "risk_score": score,
            "findings": findings if findings else ["ML found no strong patterns"],
            "confidence": 0.3  # LOW confidence on purpose
        }
