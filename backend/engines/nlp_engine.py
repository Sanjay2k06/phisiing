"""
Natural Language Processing Engine for psychological manipulation detection
(Offline-safe version – no external AI dependencies)
"""

import re
from typing import List, Dict

class NLPEngine:
    """Detects psychological manipulation and deceptive intent"""

    def __init__(self):
        self.manipulation_patterns = [
            r'\b(urgent|immediately|act now|limited time|expires|hurry)\b',
            r'\b(verify|confirm|update|suspend|lock|restrict)\b.*\b(account|payment|card)\b',
            r'\b(congratulations|winner|prize|reward|claim)\b',
            r'\b(click here|click below|tap here)\b',
            r'\b(refund|reimburs|overpay)\b',
            r'\b(security alert|unusual activity|suspicious)\b',
        ]

    async def analyze(self, content: str, mode: str) -> Dict:
        findings: List[str] = []
        risk_score = 0.0
        content_lower = content.lower()

        # Pattern-based detection
        for pattern in self.manipulation_patterns:
            if re.search(pattern, content_lower):
                risk_score += 10
                findings.append("Psychological manipulation trigger detected")

        # Excessive urgency
        urgency_words = ['urgent', 'immediately', 'now', 'hurry', 'quick', 'fast']
        urgency_count = sum(1 for w in urgency_words if w in content_lower)
        if urgency_count >= 2:
            risk_score += 15
            findings.append("High urgency pressure tactics detected")

        # Authority impersonation
        authority_terms = ['bank', 'paypal', 'amazon', 'irs', 'government', 'police', 'support']
        if any(term in content_lower for term in authority_terms):
            risk_score += 15
            findings.append("Possible authority impersonation detected")

        risk_score = min(risk_score, 100)

        verdict = (
            "High Risk" if risk_score >= 60
            else "Medium Risk" if risk_score >= 30
            else "Low Risk"
        )

        return {
            "engine_name": "NLP Engine",
            "risk_score": risk_score,
            "verdict": verdict,
            "findings": findings,
            "confidence": 0.85 if findings else 0.5
        }
