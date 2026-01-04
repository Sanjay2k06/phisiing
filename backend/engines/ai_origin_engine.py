"""
AI vs AI Origin Detection Engine
Detects whether message is likely AI-generated scam or human-written
"""

import math
from typing import Dict, List

class AIOriginEngine:
    def __init__(self):
        self.ai_markers = [
            "act now", "limited time", "verify immediately",
            "failure to comply", "avoid suspension",
            "click the link below"
        ]

    async def analyze(self, content: str, mode: str) -> Dict:
        text = content.lower()
        findings = []
        score = 0

        # 1️⃣ Over-polished grammar + urgency
        urgency_count = sum(1 for k in self.ai_markers if k in text)
        if urgency_count >= 2:
            score += 20
            findings.append("AI-style urgency phrasing detected")

        # 2️⃣ Generic personalization
        if "dear customer" in text or "dear user" in text:
            score += 15
            findings.append("Generic AI-style personalization detected")

        # 3️⃣ Sentence uniformity
        sentences = content.split(".")
        avg_len = sum(len(s) for s in sentences) / max(len(sentences), 1)
        if avg_len > 80:
            score += 15
            findings.append("Unnatural sentence uniformity (AI-like)")

        # 4️⃣ Low entropy (too clean text)
        unique_chars = len(set(text))
        entropy = unique_chars / max(len(text), 1)
        if entropy < 0.15:
            score += 20
            findings.append("Low linguistic entropy (machine-generated)")

        # Trust floor
        if score > 0 and score < 25:
            score = 25
            findings.append("AI-origin trust floor applied")

        return {
            "engine_name": "AI Origin Classifier",
            "risk_score": min(score, 100),
            "findings": findings,
            "confidence": 0.9 if findings else 0.4,
            "origin": "AI-generated scam bot" if score >= 30 else "Likely human-written"
        }
