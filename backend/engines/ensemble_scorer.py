class EnsembleScorer:
    """
    Final Verdict Gate
    NO message escapes as Safe if risk exists.
    """

    def calculate_risk_score(self, engine_results):
        max_score = max(r["risk_score"] for r in engine_results)
        avg_score = sum(r["risk_score"] for r in engine_results) / len(engine_results)

        findings = []
        for r in engine_results:
            findings.extend(r.get("findings", []))

        # 🚨 ABSOLUTE BLOCK
        if max_score >= 90:
            verdict = "Phishing Detected"
            final_score = max_score

        elif max_score >= 70:
            verdict = "Scam Detected"
            final_score = max_score

        elif avg_score >= 30:
            verdict = "Suspicious"
            final_score = avg_score

        else:
            verdict = "Safe"
            final_score = avg_score

        return {
            "risk_score": round(min(final_score, 100), 1),
            "verdict": verdict,
            "summary": verdict,
            "recommendations": self._recommend(verdict)
        }

    def _recommend(self, verdict):
        if verdict in ["Phishing Detected", "Scam Detected"]:
            return [
                "Do NOT click links",
                "Do NOT share OTP or credentials",
                "Block the sender immediately",
                "Report the message"
            ]
        elif verdict == "Suspicious":
            return [
                "Verify sender via official website",
                "Do not act on urgency",
                "Avoid clicking links"
            ]
        else:
            return [
                "Remain cautious",
                "Never share sensitive information"
            ]
