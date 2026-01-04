# backend/engines/origin_engine.py

class OriginEngine:
    """
    Determines whether a message is likely AI-generated or human-written.
    Uses linguistic and behavioral heuristics.
    """

    def analyze(self, content: str):
        score = 0
        signals = []
        text = content.lower()

        # Generic greeting patterns
        if any(p in text for p in ["dear customer", "valued user", "respected user"]):
            score += 30
            signals.append("Generic impersonation greeting")

        # Over-polished / generic tone
        if len(content.split()) > 40:
            score += 20
            signals.append("Over-detailed generic phrasing")

        # Emotionally neutral but urgent
        if "act now" in text or "limited time" in text:
            score += 20
            signals.append("Synthetic urgency pattern")

        # Lack of personalization
        if not any(p in text for p in ["your name", "order id", "last transaction"]):
            score += 10
            signals.append("Lack of personalization")

        likely_origin = "Human"
        if score >= 40:
            likely_origin = "AI-Assisted"

        return {
            "likely_origin": likely_origin,
            "confidence": min(score / 100, 1.0),
            "signals": signals
        }
