"""
Senior URL Intelligence Engine
Detects malicious, AI-generated, and scam URLs using
heuristics + entropy + trust-floor logic.
"""

import re
import math
from typing import List, Dict
from urllib.parse import urlparse

class URLEngine:
    def __init__(self):
        self.legitimate_domains = {
            'google.com', 'facebook.com', 'amazon.com', 'paypal.com',
            'microsoft.com', 'apple.com', 'netflix.com', 'linkedin.com'
        }

        self.suspicious_tlds = {
            '.tk', '.ml', '.ga', '.cf', '.gq',
            '.xyz', '.top', '.work', '.click', '.zip'
        }

        self.url_shorteners = {
            'bit.ly', 'tinyurl.com', 't.co',
            'goo.gl', 'ow.ly', 'is.gd'
        }

    # ---------------- MAIN ENTRY ----------------
    async def analyze(self, content: str, mode: str) -> Dict:
        findings = []
        risk_score = 0.0

        urls = self._extract_urls(content)

        # Trust floor: URL mode but no URL
        if mode == "url" and not urls:
            return self._result(
                60,
                ["URL mode selected but no valid URL detected"],
                0.8
            )

        if not urls:
            return self._result(
                0,
                ["No URLs found"],
                0.4
            )

        for url in urls[:5]:
            risk_score += self._analyze_single_url(url, findings)

        # 🔥 Trust Floor: ANY external unknown URL
        if urls and risk_score < 25:
            risk_score = 25
            findings.append("Unverified external link (trust floor applied)")

        return self._result(min(risk_score, 100), findings, 0.9)

    # ---------------- URL EXTRACTION ----------------
    def _extract_urls(self, content: str) -> List[str]:
        pattern = r'(https?://[^\s<>"\']+|www\.[^\s<>"\']+|[a-zA-Z0-9-]+\.[a-z]{2,})'
        return re.findall(pattern, content.lower())

    # ---------------- SINGLE URL ANALYSIS ----------------
    def _analyze_single_url(self, url: str, findings: List[str]) -> float:
        score = 0.0

        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # IP-based URL
        if re.match(r'\d{1,3}(\.\d{1,3}){3}', domain):
            score += 40
            findings.append("IP-based URL used (high risk)")

        # Suspicious TLD
        if any(domain.endswith(tld) for tld in self.suspicious_tlds):
            score += 30
            findings.append("High-risk top-level domain detected")

        # URL shortener
        if domain in self.url_shorteners:
            score += 25
            findings.append("URL shortener used (obfuscation)")

        # Look-alike domain
        score += self._check_lookalike(domain, findings)

        # Excessive subdomains
        if domain.count('.') > 3:
            score += 15
            findings.append("Excessive subdomain nesting")

        # Hyphen abuse
        if domain.count('-') >= 3:
            score += 20
            findings.append("Machine-generated domain structure")

        # Randomness / entropy
        if self._high_entropy(domain):
            score += 25
            findings.append("High entropy domain (AI-generated pattern)")

        return score

    # ---------------- LOOK-ALIKE CHECK ----------------
    def _check_lookalike(self, domain: str, findings: List[str]) -> float:
        score = 0

        substitutions = {
            'paypal': ['paypa1', 'paypai', 'paypa11'],
            'amazon': ['amaz0n', 'arnazon'],
            'google': ['g00gle', 'gooogle'],
            'microsoft': ['micros0ft', 'rnicrosoft'],
            'apple': ['app1e', 'appl3']
        }

        for legit, fakes in substitutions.items():
            if any(fake in domain for fake in fakes):
                findings.append(f"Look-alike domain mimicking {legit}")
                return 35

        for legit in self.legitimate_domains:
            base = legit.split('.')[0]
            if base in domain and legit not in domain:
                findings.append(f"Domain resembles {legit}")
                score += 30

        return score

    # ---------------- ENTROPY CHECK ----------------
    def _high_entropy(self, text: str) -> bool:
        if len(text) < 10:
            return False
        probabilities = [text.count(c) / len(text) for c in set(text)]
        entropy = -sum(p * math.log2(p) for p in probabilities)
        return entropy > 4.0

    # ---------------- RESULT FORMAT ----------------
    def _result(self, score: float, findings: List[str], confidence: float):
        return {
            "engine_name": "URL Intelligence (Senior)",
            "risk_score": score,
            "findings": findings,
            "confidence": confidence
        }
