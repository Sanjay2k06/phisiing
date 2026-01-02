"""Behavioral Analysis Engine for social engineering pattern detection"""
import re
from typing import List, Dict

class BehavioralEngine:
    """Detects social engineering tactics and coercion patterns"""
    
    async def analyze(self, content: str, mode: str) -> Dict:
        """Analyze behavioral patterns in message"""
        findings = []
        risk_score = 0.0
        
        # Check for coercion tactics
        risk_score += self._check_coercion_tactics(content, findings)
        
        # Check for urgency and time pressure
        risk_score += self._check_time_pressure(content, findings)
        
        # Check for forced actions
        risk_score += self._check_forced_actions(content, findings)
        
        # Check for emotional manipulation
        risk_score += self._check_emotional_manipulation(content, findings)
        
        # Channel-specific behavioral analysis
        if mode == 'sms' or mode == 'whatsapp':
            risk_score += self._check_mobile_scam_patterns(content, findings)
        
        # Normalize score
        risk_score = min(risk_score, 100)
        
        return {
            'engine_name': 'Behavioral Analysis',
            'risk_score': risk_score,
            'findings': findings,
            'confidence': 0.8 if len(findings) > 0 else 0.5
        }
    
    def _check_coercion_tactics(self, content: str, findings: List[str]) -> float:
        """Detect coercion and threat-based messaging"""
        score = 0.0
        content_lower = content.lower()
        
        threat_patterns = [
            (r'\b(suspend|lock|close|terminate|restrict|disable)\b.*\b(account|access|service)\b', 'Account threat detected'),
            (r'\b(legal action|lawsuit|court|attorney|lawyer)\b', 'Legal threat detected'),
            (r'\b(police|arrest|warrant|investigation)\b', 'Authority threat detected'),
            (r'\b(fine|penalty|charge|fee)\b.*\b(pay|owe)\b', 'Financial threat detected'),
        ]
        
        for pattern, message in threat_patterns:
            if re.search(pattern, content_lower):
                score += 15
                findings.append(message)
        
        return score
    
    def _check_time_pressure(self, content: str, findings: List[str]) -> float:
        """Detect artificial time pressure tactics"""
        score = 0.0
        content_lower = content.lower()
        
        # Check for deadline language
        deadline_patterns = [
            r'within (\d+) (hour|minute|day)',
            r'expires (today|tonight|soon)',
            r'before (midnight|\d+:\d+)',
            r'last chance',
            r'final (notice|warning|reminder)',
        ]
        
        deadline_count = 0
        for pattern in deadline_patterns:
            if re.search(pattern, content_lower):
                deadline_count += 1
        
        if deadline_count >= 2:
            score += 20
            findings.append(f"High time pressure detected ({deadline_count} deadline markers)")
        elif deadline_count == 1:
            score += 10
            findings.append("Time pressure tactics detected")
        
        return score
    
    def _check_forced_actions(self, content: str, findings: List[str]) -> float:
        """Detect forced immediate action requests"""
        score = 0.0
        content_lower = content.lower()
        
        action_patterns = [
            (r'\b(click|tap|press)\b.*\b(here|below|link|button)\b', 'Forced click action'),
            (r'\b(reply|respond|confirm)\b.*\b(immediately|now|asap)\b', 'Forced reply action'),
            (r'\b(download|install|update)\b.*\b(now|immediately)\b', 'Forced download action'),
            (r'\b(call|phone|contact)\b.*\b(immediately|urgently|now)\b', 'Forced contact action'),
        ]
        
        for pattern, message in action_patterns:
            if re.search(pattern, content_lower):
                score += 12
                findings.append(message)
        
        return score
    
    def _check_emotional_manipulation(self, content: str, findings: List[str]) -> float:
        """Detect emotional manipulation tactics"""
        score = 0.0
        content_lower = content.lower()
        
        # Fear-based
        fear_words = ['warning', 'alert', 'danger', 'risk', 'threat', 'breach', 'hack', 'compromise']
        fear_count = sum(1 for word in fear_words if word in content_lower)
        if fear_count >= 2:
            score += 15
            findings.append(f"Fear-based emotional manipulation ({fear_count} fear triggers)")
        
        # Greed-based
        greed_words = ['prize', 'winner', 'reward', 'bonus', 'gift', 'free', 'offer']
        greed_count = sum(1 for word in greed_words if word in content_lower)
        if greed_count >= 2:
            score += 12
            findings.append(f"Greed-based emotional manipulation ({greed_count} reward triggers)")
        
        return score
    
    def _check_mobile_scam_patterns(self, content: str, findings: List[str]) -> float:
        """Detect patterns specific to mobile scams"""
        score = 0.0
        content_lower = content.lower()
        
        mobile_patterns = [
            (r'\b(otp|pin|code|password)\b', 'OTP/credential request detected'),
            (r'\b(delivery|package|parcel)\b.*\b(confirm|verify|pending)\b', 'Fake delivery scam pattern'),
            (r'\b(won|winner|selected)\b.*\b(prize|reward|gift)\b', 'Prize scam pattern'),
            (r'\b(refund|reimbursement)\b.*\b(claim|process|verify)\b', 'Refund scam pattern'),
        ]
        
        for pattern, message in mobile_patterns:
            if re.search(pattern, content_lower):
                score += 15
                findings.append(message)
        
        return score