from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime, timezone

class DetectionRequest(BaseModel):
    """Request model for phishing detection"""
    content: str = Field(..., description="Message content to analyze")
    mode: str = Field(default="general", description="Detection mode: email, sms, whatsapp, url, general")
    email_headers: Optional[Dict[str, str]] = Field(default=None, description="Email headers for email mode")

class EngineResult(BaseModel):
    """Result from individual detection engine"""
    engine_name: str
    risk_score: float = Field(ge=0, le=100)
    findings: List[str]
    confidence: float = Field(ge=0, le=1)

class DetectionResponse(BaseModel):
    """Response model for phishing detection"""
    risk_score: float = Field(ge=0, le=100)
    verdict: str
    mode: str
    engine_results: List[EngineResult]
    summary: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    recommendations: List[str]

class AnalysisHistory(BaseModel):
    """Stored analysis for history"""
    id: str
    content_preview: str
    mode: str
    risk_score: float
    verdict: str
    timestamp: str