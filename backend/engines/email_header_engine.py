"""Email Header Integrity Engine for spoofing detection"""
import re
from typing import List, Dict, Optional

class EmailHeaderEngine:
    """Detects email spoofing and header manipulation"""
    
    async def analyze(self, content: str, mode: str, headers: Optional[Dict[str, str]]) -> Dict:
        """Analyze email headers for spoofing indicators"""
        findings = []
        risk_score = 0.0
        
        if mode != 'email' or not headers:
            return {
                'engine_name': 'Email Header Analysis',
                'risk_score': 0.0,
                'findings': ['Not applicable for non-email messages'],
                'confidence': 0.0
            }
        
        # Check SPF, DKIM, DMARC
        risk_score += self._check_authentication(headers, findings)
        
        # Check sender domain
        risk_score += self._check_sender_domain(headers, findings)
        
        # Check reply-to mismatch
        risk_score += self._check_reply_to(headers, findings)
        
        # Check routing anomalies
        risk_score += self._check_routing(headers, findings)
        
        # Normalize score
        risk_score = min(risk_score, 100)
        
        return {
            'engine_name': 'Email Header Analysis',
            'risk_score': risk_score,
            'findings': findings,
            'confidence': 0.95 if len(findings) > 0 else 0.7
        }
    
    def _check_authentication(self, headers: Dict[str, str], findings: List[str]) -> float:
        """Check SPF, DKIM, DMARC authentication"""
        score = 0.0
        
        # Check SPF
        spf = headers.get('spf', '').lower()
        if 'fail' in spf:
            score += 25
            findings.append("SPF authentication failed")
        elif 'softfail' in spf:
            score += 15
            findings.append("SPF soft fail detected")
        
        # Check DKIM
        dkim = headers.get('dkim', '').lower()
        if 'fail' in dkim:
            score += 25
            findings.append("DKIM signature verification failed")
        
        # Check DMARC
        dmarc = headers.get('dmarc', '').lower()
        if 'fail' in dmarc:
            score += 20
            findings.append("DMARC policy check failed")
        
        return score
    
    def _check_sender_domain(self, headers: Dict[str, str], findings: List[str]) -> float:
        """Check sender domain for spoofing"""
        score = 0.0
        
        from_header = headers.get('from', '').lower()
        return_path = headers.get('return-path', '').lower()
        
        # Extract domains
        from_domain = self._extract_domain(from_header)
        return_domain = self._extract_domain(return_path)
        
        # Check if domains match
        if from_domain and return_domain and from_domain != return_domain:
            score += 20
            findings.append(f"Domain mismatch: From ({from_domain}) vs Return-Path ({return_domain})")
        
        # Check for common spoofing domains
        suspicious_domains = ['gmail', 'yahoo', 'outlook', 'hotmail', 'paypal', 'amazon']
        for domain in suspicious_domains:
            if domain in from_domain and not from_domain.endswith(f'{domain}.com'):
                score += 25
                findings.append(f"Suspicious domain mimicking {domain}")
                break
        
        return score
    
    def _check_reply_to(self, headers: Dict[str, str], findings: List[str]) -> float:
        """Check for reply-to address mismatch"""
        score = 0.0
        
        from_header = headers.get('from', '').lower()
        reply_to = headers.get('reply-to', '').lower()
        
        if reply_to and reply_to != from_header:
            from_domain = self._extract_domain(from_header)
            reply_domain = self._extract_domain(reply_to)
            
            if from_domain != reply_domain:
                score += 20
                findings.append(f"Reply-To address differs from sender domain")
        
        return score
    
    def _check_routing(self, headers: Dict[str, str], findings: List[str]) -> float:
        """Check for routing anomalies"""
        score = 0.0
        
        received = headers.get('received', '').lower()
        
        # Check for suspicious countries/regions in routing
        suspicious_regions = ['nigeria', 'russia', 'china', 'vietnam', '.ru', '.cn']
        for region in suspicious_regions:
            if region in received:
                score += 10
                findings.append(f"Routing through suspicious region detected")
                break
        
        # Check for excessive hops
        hop_count = received.count('received:')
        if hop_count > 10:
            score += 8
            findings.append(f"Excessive routing hops detected ({hop_count})")
        
        return score
    
    def _extract_domain(self, email_string: str) -> str:
        """Extract domain from email address"""
        match = re.search(r'@([\w.-]+)', email_string)
        return match.group(1) if match else ''