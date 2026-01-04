from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

# ---------------- REQUEST ----------------

class DetectionRequest(BaseModel):
    content: str
    mode: str = "general"
    email_headers: Optional[Dict[str, str]] = None

# ---------------- ENGINE RESULT ----------------

class EngineResult(BaseModel):
    engine_name: str
    risk_score: float = Field(ge=0, le=100)
    findings: List[str]
    confidence: float = Field(ge=0, le=1)

    # ✅ STEP-3: Explainability
    timeline: List[str] = []

# ---------------- RESPONSE ----------------

class DetectionResponse(BaseModel):
    risk_score: float = Field(ge=0, le=100)
    verdict: str
    mode: str

    engine_results: List[EngineResult]

    # ✅ summary is DICT (already fixed)
    summary: Dict[str, Any]

    recommendations: List[str]

    # ✅ STEP-3: Final timeline
    timeline: List[str] = []

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
