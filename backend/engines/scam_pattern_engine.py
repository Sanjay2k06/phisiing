"""Scam Pattern Engine for real-world fraud scenario detection"""
import re
from typing import List, Dict

class ScamPatternEngine:
    """Detects common real-world scam and fraud patterns"""
    
    def __init__(self):
        self.scam_patterns = {
            'delivery_scam': {
                'patterns': [
                    r'\b(delivery|package|parcel|shipment)\b.*\b(pending|failed|held|waiting)\b',
                    r'\b(courier|fedex|ups|dhl|usps)\b.*\b(confirm|verify|schedule)\b',
                    r'\b(track|tracking)\b.*\b(number|code|link)\b',
                ],
                'keywords': ['delivery', 'package', 'parcel', 'courier', 'fedex', 'ups'],
                'score': 20,
                'message': 'Fake delivery/package scam pattern detected'
            },
            'otp_scam': {
                'patterns': [
                    r'\b(otp|one.time.password|verification.code|pin)\b',
                    r'\bcode.*(is|:)\s*\d{4,6}\b',
                    r'\b(enter|provide|share|send)\b.*\b(otp|code|pin)\b',
                ],
                'keywords': ['otp', 'verification code', 'pin', 'one-time'],
                'score': 25,
                'message': 'OTP/credential theft scam detected'
            },
            'refund_scam': {
                'patterns': [
                    r'\b(refund|reimbursement|overpayment)\b.*\b(pending|process|claim)\b',
                    r'\b(entitled|eligible|qualify)\b.*\b(refund|money|payment)\b',
                    r'\b(refund)\b.*\b(\$|amount|usd|inr)\b',
                ],
                'keywords': ['refund', 'reimbursement', 'overpayment'],
                'score': 22,
                'message': 'Fake refund/reimbursement scam detected'
            },
            'job_fraud': {
                'patterns': [
                    r'\b(job|work|employment)\b.*\b(offer|opportunity|position)\b',
                    r'\b(earn|make)\b.*\b(\$|money|cash)\b.*\b(home|online)\b',
                    r'\b(selected|chosen|hired)\b.*\b(interview|position)\b',
                ],
                'keywords': ['job offer', 'work from home', 'earn money', 'employment'],
                'score': 18,
                'message': 'Job offer fraud pattern detected'
            },
            'payment_trap': {
                'patterns': [
                    r'\b(payment|transaction)\b.*\b(failed|declined|error|issue)\b',
                    r'\b(update|verify|confirm)\b.*\b(payment|card|billing)\b',
                    r'\b(subscription|membership)\b.*\b(renew|expire|cancel)\b',
                ],
                'keywords': ['payment failed', 'card declined', 'subscription', 'billing'],
                'score': 20,
                'message': 'Payment failure trap scam detected'
            },
            'prize_scam': {
                'patterns': [
                    r'\b(congratulations|winner|won|selected)\b',
                    r'\b(prize|reward|gift|bonus)\b.*\b(claim|collect|receive)\b',
                    r'\b(lottery|sweepstakes|contest)\b',
                ],
                'keywords': ['congratulations', 'winner', 'prize', 'lottery'],
                'score': 23,
                'message': 'Prize/lottery scam pattern detected'
            },
            'account_verification': {
                'patterns': [
                    r'\b(verify|confirm|update)\b.*\b(account|identity|information)\b',
                    r'\b(suspended|locked|restricted)\b.*\b(account|access)\b',
                    r'\b(unusual|suspicious)\b.*\b(activity|login|access)\b',
                ],
                'keywords': ['verify account', 'account suspended', 'unusual activity'],
                'score': 21,
                'message': 'Account verification phishing detected'
            },
        }
    
    async def analyze(self, content: str, mode: str) -> Dict:
        """Analyze content for known scam patterns"""
        findings = []
        risk_score = 0.0
        detected_patterns = []
        
        content_lower = content.lower()
        
        # Check each scam pattern
        for scam_type, scam_data in self.scam_patterns.items():
            detected = False
            
            # Check regex patterns
            for pattern in scam_data['patterns']:
                if re.search(pattern, content_lower):
                    detected = True
                    break
            
            # Check keywords
            if not detected:
                keyword_matches = sum(1 for kw in scam_data['keywords'] if kw in content_lower)
                if keyword_matches >= 2:
                    detected = True
            
            if detected:
                risk_score += scam_data['score']
                findings.append(scam_data['message'])
                detected_patterns.append(scam_type)
        
        # Multiple scam patterns = higher risk
        if len(detected_patterns) >= 2:
            risk_score += 15
            findings.append(f"Multiple scam patterns detected: {', '.join(detected_patterns[:3])}")
        
        # Check for money requests
        if re.search(r'\b(pay|send|transfer|wire)\b.*\b(money|cash|payment|\$|usd)\b', content_lower):
            risk_score += 18
            findings.append("Direct money request detected")
        
        # Check for personal info requests
        personal_info = ['ssn', 'social security', 'credit card', 'card number', 'cvv', 'password', 'pin']
        if any(info in content_lower for info in personal_info):
            risk_score += 25
            findings.append("Sensitive personal information request detected")
        
        # Normalize score
        risk_score = min(risk_score, 100)
        
        return {
            'engine_name': 'Scam Pattern Recognition',
            'risk_score': risk_score,
            'findings': findings,
            'confidence': 0.9 if len(findings) > 0 else 0.4
        }