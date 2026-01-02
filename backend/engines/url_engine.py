"""URL Intelligence Engine for malicious link detection"""
import re
from typing import List, Dict
from urllib.parse import urlparse

class URLEngine:
    """Detects malicious URLs and suspicious link patterns"""
    
    def __init__(self):
        self.legitimate_domains = {
            'google.com', 'facebook.com', 'amazon.com', 'paypal.com',
            'microsoft.com', 'apple.com', 'netflix.com', 'linkedin.com'
        }
        self.suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work']
    
    async def analyze(self, content: str, mode: str) -> Dict:
        """Analyze URLs in content"""
        findings = []
        risk_score = 0.0
        
        # Extract URLs
        urls = self._extract_urls(content)
        
        if not urls:
            if mode == 'url':
                findings.append("No valid URL detected")
                return {
                    'engine_name': 'URL Intelligence',
                    'risk_score': 0.0,
                    'findings': findings,
                    'confidence': 0.3
                }
            else:
                findings.append("No URLs found in message")
                return {
                    'engine_name': 'URL Intelligence',
                    'risk_score': 0.0,
                    'findings': findings,
                    'confidence': 0.5
                }
        
        # Analyze each URL
        for url in urls[:5]:  # Limit to 5 URLs
            url_score = self._analyze_single_url(url, findings)
            risk_score += url_score
        
        # Normalize score
        risk_score = min(risk_score, 100)
        
        return {
            'engine_name': 'URL Intelligence',
            'risk_score': risk_score,
            'findings': findings,
            'confidence': 0.9 if len(findings) > 0 else 0.6
        }
    
    def _extract_urls(self, content: str) -> List[str]:
        """Extract URLs from content"""
        # URL pattern
        url_pattern = r'https?://[^\s<>"\']+'
        url_pattern += r'|www\.[^\s<>"\']+'
        url_pattern += r'|[a-zA-Z0-9-]+\.[a-z]{2,}(?:/[^\s<>"\']*)?' 
        
        urls = re.findall(url_pattern, content, re.IGNORECASE)
        return urls
    
    def _analyze_single_url(self, url: str, findings: List[str]) -> float:
        """Analyze a single URL for threats"""
        score = 0.0
        
        try:
            # Add scheme if missing
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Check for suspicious TLDs
            for tld in self.suspicious_tlds:
                if domain.endswith(tld):
                    score += 20
                    findings.append(f"Suspicious TLD detected: {tld}")
                    break
            
            # Check for look-alike domains
            lookalike_score = self._check_lookalike_domain(domain, findings)
            score += lookalike_score
            
            # Check for IP address instead of domain
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
                score += 25
                findings.append("IP address used instead of domain name")
            
            # Check for URL shorteners (potential obfuscation)
            shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly']
            if any(short in domain for short in shorteners):
                score += 15
                findings.append("URL shortener detected (potential obfuscation)")
            
            # Check for excessive subdomains
            subdomain_count = domain.count('.')
            if subdomain_count > 3:
                score += 12
                findings.append(f"Excessive subdomains detected ({subdomain_count})")
            
            # Check for suspicious characters
            if any(char in domain for char in ['@', '-', '_']):
                suspicious_chars = [c for c in ['@', '-', '_'] if c in domain]
                if len(suspicious_chars) >= 2 or '@' in domain:
                    score += 10
                    findings.append(f"Suspicious characters in domain: {suspicious_chars}")
        
        except Exception as e:
            findings.append(f"URL parsing error: {str(e)[:50]}")
            score += 5
        
        return score
    
    def _check_lookalike_domain(self, domain: str, findings: List[str]) -> float:
        """Check for domains that mimic legitimate ones"""
        score = 0.0
        
        # Common character substitutions
        substitutions = {
            'paypal': ['paypa1', 'paypai', 'paypa-', 'paypa11'],
            'amazon': ['amaz0n', 'arnazon', 'amazom', 'amazon-'],
            'google': ['gooogle', 'g00gle', 'googie', 'gogle'],
            'microsoft': ['micros0ft', 'microsft', 'rnicrosoff'],
            'apple': ['app1e', 'appl3', 'apple-'],
        }
        
        for legit, fakes in substitutions.items():
            if any(fake in domain for fake in fakes):
                score += 30
                findings.append(f"Look-alike domain detected (mimics {legit})")
                return score
        
        # Check for legitimate domain with extra characters
        for legit in self.legitimate_domains:
            if legit.replace('.com', '') in domain and legit not in domain:
                score += 25
                findings.append(f"Domain closely resembles {legit}")
                break
        
        return score