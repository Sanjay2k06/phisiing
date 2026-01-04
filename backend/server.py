from fastapi import FastAPI, APIRouter, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

import re
import math
from datetime import datetime, timezone
from urllib.parse import urlparse
import logging

# --------------------------------------------------
# RATE LIMITER
# --------------------------------------------------
limiter = Limiter(key_func=get_remote_address)

# --------------------------------------------------
# APP
# --------------------------------------------------
app = FastAPI(
    title="CyberSentinel AI – ENTERPRISE PHISHING DEFENSE",
    version="FINAL-10.0"
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

api = APIRouter(prefix="/api")

# --------------------------------------------------
# LOGGING
# --------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CyberSentinel")

# --------------------------------------------------
# MODELS (FRONTEND SAFE)
# --------------------------------------------------
class DetectionRequest(BaseModel):
    content: str
    mode: str = "general"

class EngineResult(BaseModel):
    engine_name: str
    risk_score: float
    findings: list
    confidence: float

class DetectionResponse(BaseModel):
    risk_score: int
    verdict: str
    mode: str
    engine_results: list
    summary: dict
    recommendations: list
    timestamp: datetime

# --------------------------------------------------
# NORMALIZATION (ANTI-BYPASS)
# --------------------------------------------------
def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = text.replace("0", "o").replace("1", "i").replace("@", "a")
    return text.strip()

# --------------------------------------------------
# URL EXTRACTION
# --------------------------------------------------
def extract_urls(text):
    return re.findall(r"https?://[^\s]+", text)

# --------------------------------------------------
# SHANNON ENTROPY
# --------------------------------------------------
def shannon_entropy(s):
    if not s:
        return 0
    freq = {c: s.count(c) for c in set(s)}
    return -sum((f/len(s)) * math.log2(f/len(s)) for f in freq.values())

# --------------------------------------------------
# BRAND LIST
# --------------------------------------------------
BRANDS = ["amazon", "paypal", "google", "facebook", "instagram", "microsoft"]

# --------------------------------------------------
# ENGINE 1: URL INTELLIGENCE
# --------------------------------------------------
def url_engine(url):
    findings = []
    score = 0
    parsed = urlparse(url)
    domain = parsed.netloc

    bad_tlds = [".xyz", ".tk", ".ml", ".ga", ".cf", ".top", ".click"]
    if any(domain.endswith(tld) for tld in bad_tlds):
        score += 40
        findings.append(f"Suspicious TLD: {domain}")

    if re.search(r"\d+\.\d+\.\d+\.\d+", domain):
        score += 30
        findings.append("IP-based URL detected")

    if len(domain.split(".")) > 3:
        score += 20
        findings.append("Randomized / deep subdomain")

    if shannon_entropy(parsed.path) > 3.5 and len(parsed.path) > 15:
        score += 25
        findings.append("Obfuscated high-entropy URL path")

    if parsed.query:
        score += 15
        findings.append("Tracking / redirect parameters")

    for brand in BRANDS:
        if brand in domain and not domain.endswith(f"{brand}.com"):
            score += 30
            findings.append(f"Brand impersonation: {brand}")

    return EngineResult(
        engine_name="URL Intelligence Engine",
        risk_score=min(score, 100),
        findings=findings or ["URL structure appears normal"],
        confidence=round(min(score, 100) / 100, 2)
    )

# --------------------------------------------------
# ENGINE 2: MARKET / GIFT SCAM
# --------------------------------------------------
def market_scam_engine(text):
    score = 0
    findings = []

    keywords = [
        "gift card", "free reward", "won", "winner",
        "claim now", "limited offer", "upi",
        "telegram", "advance payment"
    ]

    for k in keywords:
        if k in text:
            score += 15
            findings.append(f"Market scam keyword: {k}")

    return EngineResult(
        engine_name="Marketplace Scam Engine",
        risk_score=min(score, 90),
        findings=findings or ["No marketplace scam patterns"],
        confidence=round(min(score, 90) / 100, 2)
    )

# --------------------------------------------------
# ENGINE 3: SOCIAL ENGINEERING
# --------------------------------------------------
def social_engineering_engine(text):
    score = 0
    findings = []

    if any(k in text for k in ["verify", "confirm", "login", "account"]):
        score += 25
        findings.append("Credential harvesting language")

    if any(k in text for k in ["urgent", "immediately", "expires", "act now"]):
        score += 20
        findings.append("Urgency manipulation")

    if "otp" in text:
        score += 40
        findings.append("OTP theft attempt")

    return EngineResult(
        engine_name="Social Engineering Engine",
        risk_score=min(score, 95),
        findings=findings or ["No social engineering patterns"],
        confidence=round(min(score, 95) / 100, 2)
    )

# --------------------------------------------------
# ENGINE 4: ADVANCE FEE / PRIZE SCAM (HARD RULE)
# --------------------------------------------------
def advance_fee_scam_engine(text):
    reward = any(k in text for k in [
        "won", "winner", "prize", "lottery", "gift", "reward"
    ])

    money = any(k in text for k in [
        "processing fee", "small fee", "pay", "payment",
        "bank details", "account number", "upi"
    ])

    urgency = any(k in text for k in [
        "act now", "limited time", "expires", "immediately"
    ])

    if reward and money:
        return EngineResult(
            engine_name="Advance Fee Scam Engine (Hard Rule)",
            risk_score=95,
            findings=["Prize + payment request detected"],
            confidence=1.0
        )

    if reward and urgency:
        return EngineResult(
            engine_name="Advance Fee Scam Engine (Hard Rule)",
            risk_score=85,
            findings=["Prize + urgency manipulation detected"],
            confidence=0.9
        )

    return EngineResult(
        engine_name="Advance Fee Scam Engine",
        risk_score=0,
        findings=["No advance-fee scam indicators"],
        confidence=0.3
    )

# --------------------------------------------------
# AI vs AI CONSENSUS
# --------------------------------------------------
def ai_consensus(results):
    high = sum(1 for r in results if r.risk_score >= 60)
    if high >= 2:
        return True, 95, "Multiple engines agree on phishing"
    return False, None, None

# --------------------------------------------------
# ANALYSIS CORE
# --------------------------------------------------
@api.post("/analyze", response_model=DetectionResponse)
@limiter.limit("10/minute")
async def analyze(request: Request, payload: DetectionRequest):
    try:
        text = normalize_text(payload.content)
        urls = extract_urls(text)

        engines = []

        for url in urls:
            engines.append(url_engine(url))

        engines.append(market_scam_engine(text))
        engines.append(social_engineering_engine(text))
        engines.append(advance_fee_scam_engine(text))

        max_score = max(e.risk_score for e in engines)

        # Zero-trust URL floor
        if urls and max_score < 70:
            max_score = 70
            engines.append(EngineResult(
                engine_name="Zero Trust Policy",
                risk_score=70,
                findings=["Unknown URLs treated as high risk"],
                confidence=1.0
            ))

        triggered, forced, reason = ai_consensus(engines)
        if triggered:
            max_score = forced
            engines.append(EngineResult(
                engine_name="AI-vs-AI Consensus",
                risk_score=forced,
                findings=[reason],
                confidence=1.0
            ))

        verdict = "Phishing Detected" if max_score >= 70 else "Likely Safe"

        return DetectionResponse(
            risk_score=int(max_score),
            verdict=verdict,
            mode=payload.mode,
            engine_results=[e.model_dump() for e in engines],
            summary={
                "overall_intent": verdict,
                "analysis_engines_used": len(engines),
                "ai_vs_ai": triggered
            },
            recommendations=[
                "Do NOT click the link",
                "Block sender/domain",
                "Report as phishing",
                "Never share OTP or credentials"
            ] if verdict == "Phishing Detected" else ["No action required"],
            timestamp=datetime.now(timezone.utc)
        )

    except Exception as e:
        logger.exception("Analysis failed")
        raise HTTPException(status_code=500, detail=str(e))

# --------------------------------------------------
# ROOT
# --------------------------------------------------
@api.get("/")
async def health():
    return {
        "status": "RUNNING",
        "security_level": "ENTERPRISE+",
        "engines": [
            "URL Intelligence",
            "Marketplace Scam",
            "Social Engineering",
            "Advance Fee Scam (Hard Rule)",
            "AI-vs-AI Consensus"
        ]
    }

app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests"}
    )
