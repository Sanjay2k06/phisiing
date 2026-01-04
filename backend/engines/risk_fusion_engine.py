# backend/engines/risk_fusion_engine.py

class RiskFusionEngine:
    """
    Combines all engine outputs into a final verdict.
    Uses rule-priority instead of simple averaging.
    """

    def calculate(self, base_score, intent, scam_type_detected):
        risk_score = base_score

        # Hard rules override averages
        if intent.get("malicious_intent"):
            risk_score = max(risk_score, 70)

        if scam_type_detected:
            risk_score = max(risk_score, 80)

        # Verdict mapping
        if risk_score >= 80:
            verdict = "Critical – Automated Scam"
        elif risk_score >= 60:
            verdict = "Malicious"
        elif risk_score >= 35:
            verdict = "Suspicious"
        else:
            verdict = "Clean"

        return {
            "final_risk_score": risk_score,
            "verdict": verdict
        }
