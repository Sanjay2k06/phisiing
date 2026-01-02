"""Natural Language Processing Engine for psychological manipulation detection"""
import re
from typing import List, Dict
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
import uuid

class NLPEngine:
    """Detects psychological manipulation and deceptive intent"""
    
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        self.manipulation_patterns = [
            r'\b(urgent|immediately|act now|limited time|expires|hurry)\b',
            r'\b(verify|confirm|update|suspend|lock|restrict)\b.*\b(account|payment|card)\b',
            r'\b(congratulations|winner|prize|reward|claim)\b',
            r'\b(click here|click below|tap here)\b',
            r'\b(refund|reimburs|overpay)\b',
            r'\b(security alert|unusual activity|suspicious)\b',
        ]
    
    async def analyze(self, content: str, mode: str) -> Dict:
        """Analyze content for psychological manipulation"""
        findings = []
        risk_score = 0.0
        
        # Pattern-based detection
        pattern_score = self._check_manipulation_patterns(content, findings)
        risk_score += pattern_score
        
        # AI-powered analysis
        ai_score = await self._ai_psychological_analysis(content, mode, findings)
        risk_score += ai_score
        
        # Normalize score
        risk_score = min(risk_score, 100)
        
        return {
            'engine_name': 'NLP Engine',
            'risk_score': risk_score,
            'findings': findings,
            'confidence': 0.85 if len(findings) > 0 else 0.5
        }
    
    def _check_manipulation_patterns(self, content: str, findings: List[str]) -> float:
        """Check for known manipulation patterns"""
        score = 0.0
        content_lower = content.lower()
        
        for pattern in self.manipulation_patterns:
            matches = re.findall(pattern, content_lower)
            if matches:
                score += 8
                findings.append(f"Manipulation trigger detected: '{matches[0]}'")
        
        # Check for excessive urgency
        urgency_words = ['urgent', 'immediately', 'now', 'hurry', 'quick', 'fast']
        urgency_count = sum(1 for word in urgency_words if word in content_lower)
        if urgency_count >= 2:
            score += 12
            findings.append(f"High urgency pressure detected ({urgency_count} urgency markers)")
        
        # Check for authority impersonation
        authority_terms = ['bank', 'paypal', 'amazon', 'irs', 'government', 'police', 'support team']
        authority_count = sum(1 for term in authority_terms if term in content_lower)
        if authority_count >= 1:
            score += 10
            findings.append(f"Authority impersonation indicators found")
        
        return score
    
    async def _ai_psychological_analysis(self, content: str, mode: str, findings: List[str]) -> float:
        """Use AI to detect sophisticated psychological manipulation"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=str(uuid.uuid4()),
                system_message="""You are a cybersecurity expert analyzing messages for phishing and scam patterns.
                Analyze the psychological manipulation techniques used. Focus on:
                - Fear appeals (threats, warnings, account suspension)
                - Urgency tactics (time pressure, limited offers)
                - Authority abuse (impersonating legitimate organizations)
                - Reward promises (prizes, refunds, gifts)
                - Social proof manipulation
                
                Respond in this exact format:
                RISK_SCORE: [0-50]
                FINDINGS:
                - [finding 1]
                - [finding 2]
                """
            ).with_model('openai', 'gpt-4o')
            
            prompt = f"""Analyze this {mode} message for psychological manipulation:

{content}

Provide risk score (0-50) and list specific manipulation techniques found."""
            
            response = await chat.send_message(UserMessage(text=prompt))
            
            # Parse AI response
            score = self._parse_ai_score(response)
            ai_findings = self._parse_ai_findings(response)
            findings.extend(ai_findings)
            
            return score
        except Exception as e:
            findings.append(f"AI analysis unavailable: {str(e)[:50]}")
            return 0.0
    
    def _parse_ai_score(self, response: str) -> float:
        """Extract risk score from AI response"""
        try:
            match = re.search(r'RISK_SCORE:\s*(\d+)', response)
            if match:
                return float(match.group(1))
        except:
            pass
        return 0.0
    
    def _parse_ai_findings(self, response: str) -> List[str]:
        """Extract findings from AI response"""
        findings = []
        try:
            # Find all bullet points after FINDINGS:
            lines = response.split('\n')
            in_findings = False
            for line in lines:
                if 'FINDINGS:' in line:
                    in_findings = True
                    continue
                if in_findings and line.strip().startswith('-'):
                    finding = line.strip().lstrip('-').strip()
                    if finding:
                        findings.append(finding)
        except:
            pass
        return findings[:5]  # Limit to 5 findings