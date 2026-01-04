from typing import List, Dict

def ai_voting_override(engine_results: List[Dict]) -> Dict:
    """
    Forces phishing if majority engines show danger.
    """

    high_risk_engines = [
        r for r in engine_results if r["risk_score"] >= 60
    ]

    if len(high_risk_engines) >= 2:
        return {
            "triggered": True,
            "score": 92.0,
            "reason": "AI voting override: multiple engines agree"
        }

    return {
        "triggered": False,
        "score": None,
        "reason": None
    }
