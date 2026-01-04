def apply_ai_consensus(
    ml_score: int,
    rule_scores: list,
    current_verdict: str
):
    """
    Resolves conflicts between ML engine and rule-based engines
    """

    consensus = {
        "ai_conflict": False,
        "final_verdict": current_verdict,
        "confidence_adjustment": 0
    }

    if not rule_scores:
        return consensus

    rule_max = max(rule_scores)

    # 🔥 AI vs AI CONFLICT DETECTION
    if ml_score >= 70 and rule_max < 40:
        consensus["ai_conflict"] = True
        consensus["final_verdict"] = "Suspicious"
        consensus["confidence_adjustment"] = -10

    elif ml_score < 30 and rule_max >= 70:
        consensus["ai_conflict"] = True
        consensus["final_verdict"] = "Phishing Detected"
        consensus["confidence_adjustment"] = +10

    return consensus
