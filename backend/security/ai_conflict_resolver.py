from typing import List, Dict


def apply_ai_consensus(engine_results: List[Dict], current_score: float):
    """
    AI vs AI CONSENSUS ENGINE

    If multiple independent engines show suspicious behavior,
    escalate risk even if individual scores are medium.
    """

    suspicious_engines = [
        r for r in engine_results if r.get("risk_score", 0) >= 20
    ]

    # 🚨 If 3 or more engines agree → escalate
    if len(suspicious_engines) >= 3:
        return {
            "score": max(current_score, 60),
            "triggered": True,
            "reason": "Multiple AI engines independently detected suspicious intent"
        }

    return {
        "score": current_score,
        "triggered": False,
        "reason": None
    }
