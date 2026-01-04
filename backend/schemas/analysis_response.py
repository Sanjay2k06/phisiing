from typing import List, Dict


def apply_ai_consensus(engine_results: List[Dict], current_score: float):
    """
    If multiple engines independently signal risk,
    escalate even if each score is medium.
    """

    contributing_engines = [
        r for r in engine_results if r["risk_score"] >= 20
    ]

    if len(contributing_engines) >= 3:
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
