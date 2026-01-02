"""Ensemble Risk Scoring Algorithm"""
from typing import List, Dict
import math

class EnsembleScorer:
    """Combines signals from all engines into final risk score and verdict"""
    
    def calculate_risk_score(self, engine_results: List[Dict]) -> Dict:
        """Calculate ensemble risk score and verdict"""
        
        if not engine_results:
            return {
                'risk_score': 0.0,
                'verdict': 'Unknown',
                'summary': 'No analysis data available'
            }
        
        # Weighted average based on confidence
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for result in engine_results:
            weight = result.get('confidence', 0.5)
            score = result.get('risk_score', 0.0)
            total_weighted_score += score * weight
            total_weight += weight
        
        base_score = total_weighted_score / total_weight if total_weight > 0 else 0.0
        
        # Apply ensemble boost for high-confidence detections
        high_risk_engines = sum(1 for r in engine_results if r.get('risk_score', 0) > 50)
        if high_risk_engines >= 3:
            base_score = min(base_score * 1.2, 100)
        elif high_risk_engines >= 2:
            base_score = min(base_score * 1.1, 100)
        
        # Calculate final score
        final_score = round(base_score, 1)
        
        # Determine verdict
        verdict = self._determine_verdict(final_score, engine_results)
        
        # Generate summary
        summary = self._generate_summary(final_score, verdict, engine_results)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(verdict, engine_results)
        
        return {
            'risk_score': final_score,
            'verdict': verdict,
            'summary': summary,
            'recommendations': recommendations
        }
    
    def _determine_verdict(self, score: float, engine_results: List[Dict]) -> str:
        """Determine verdict based on risk score and engine findings"""
        
        # Check for critical findings
        critical_patterns = [
            'SPF authentication failed',
            'DKIM signature verification failed',
            'Sensitive personal information request detected',
            'Look-alike domain detected',
            'Multiple scam patterns detected'
        ]
        
        all_findings = []
        for result in engine_results:
            all_findings.extend(result.get('findings', []))
        
        has_critical = any(any(pattern in finding for pattern in critical_patterns) for finding in all_findings)
        
        if score >= 70 or has_critical:
            return 'Phishing Detected'
        elif score >= 50:
            return 'Scam Detected'
        elif score >= 30:
            return 'Suspicious'
        else:
            return 'Safe'
    
    def _generate_summary(self, score: float, verdict: str, engine_results: List[Dict]) -> str:
        """Generate human-readable summary"""
        
        total_findings = sum(len(r.get('findings', [])) for r in engine_results)
        active_engines = sum(1 for r in engine_results if r.get('risk_score', 0) > 0)
        
        if verdict == 'Phishing Detected':
            return f"High risk phishing attempt detected with {total_findings} security concerns across {active_engines} analysis engines. This message exhibits multiple threat indicators and should be treated as malicious."
        elif verdict == 'Scam Detected':
            return f"Scam attempt identified with {total_findings} suspicious indicators. This message uses common fraud patterns and manipulation tactics. Exercise extreme caution."
        elif verdict == 'Suspicious':
            return f"Message shows {total_findings} suspicious characteristics. While not definitively malicious, this message exhibits concerning patterns that warrant careful verification before taking any action."
        else:
            return f"Message appears legitimate with minimal risk indicators. However, always verify sender identity and avoid sharing sensitive information."
    
    def _generate_recommendations(self, verdict: str, engine_results: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        if verdict == 'Phishing Detected':
            recommendations.extend([
                "Do not click any links or download attachments",
                "Do not reply or provide any personal information",
                "Report this message to your email provider or IT security team",
                "Delete this message immediately",
                "If you've already clicked links, change your passwords immediately"
            ])
        elif verdict == 'Scam Detected':
            recommendations.extend([
                "Do not respond to this message",
                "Verify sender identity through official channels",
                "Do not provide any personal or financial information",
                "Block the sender and report as spam",
                "Contact the organization directly using verified contact information"
            ])
        elif verdict == 'Suspicious':
            recommendations.extend([
                "Verify the sender's identity before responding",
                "Do not click links - manually type URLs instead",
                "Contact the sender through known, trusted channels",
                "Look for additional verification from official sources",
                "Be cautious of urgent requests for action or information"
            ])
        else:
            recommendations.extend([
                "Always verify unexpected requests, even from known contacts",
                "Hover over links to preview destination before clicking",
                "Never share passwords, OTPs, or sensitive data via email/SMS",
                "Enable two-factor authentication for important accounts"
            ])
        
        return recommendations[:5]  # Return top 5 recommendations