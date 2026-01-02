from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from datetime import datetime, timezone

from models import DetectionRequest, DetectionResponse, EngineResult, AnalysisHistory
from engines.nlp_engine import NLPEngine
from engines.url_engine import URLEngine
from engines.behavioral_engine import BehavioralEngine
from engines.email_header_engine import EmailHeaderEngine
from engines.scam_pattern_engine import ScamPatternEngine
from engines.ensemble_scorer import EnsembleScorer

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI(title="CyberSentinel AI - Phishing Defense API")
api_router = APIRouter(prefix="/api")

# Initialize detection engines
nlp_engine = NLPEngine()
url_engine = URLEngine()
behavioral_engine = BehavioralEngine()
email_header_engine = EmailHeaderEngine()
scam_pattern_engine = ScamPatternEngine()
ensemble_scorer = EnsembleScorer()

logger = logging.getLogger(__name__)

@api_router.get("/")
async def root():
    return {
        "message": "CyberSentinel AI - Phishing Defense System",
        "version": "1.0.0",
        "status": "operational"
    }

@api_router.post("/analyze", response_model=DetectionResponse)
async def analyze_message(request: DetectionRequest):
    """
    Analyze message for phishing/scam patterns
    
    Modes:
    - email: Full email with headers
    - sms: SMS/text message
    - whatsapp: WhatsApp-style message
    - url: URL-only analysis
    - general: General message analysis
    """
    try:
        logger.info(f"Analyzing message in {request.mode} mode")
        
        # Run all applicable engines
        engine_results = []
        
        # NLP Engine (always run)
        nlp_result = await nlp_engine.analyze(request.content, request.mode)
        engine_results.append(EngineResult(**nlp_result))
        
        # URL Engine (always run)
        url_result = await url_engine.analyze(request.content, request.mode)
        engine_results.append(EngineResult(**url_result))
        
        # Behavioral Engine (always run)
        behavioral_result = await behavioral_engine.analyze(request.content, request.mode)
        engine_results.append(EngineResult(**behavioral_result))
        
        # Email Header Engine (only for email mode)
        if request.mode == 'email':
            email_result = await email_header_engine.analyze(
                request.content, 
                request.mode, 
                request.email_headers
            )
            engine_results.append(EngineResult(**email_result))
        
        # Scam Pattern Engine (always run)
        scam_result = await scam_pattern_engine.analyze(request.content, request.mode)
        engine_results.append(EngineResult(**scam_result))
        
        # Calculate ensemble score
        ensemble_result = ensemble_scorer.calculate_risk_score(
            [r.model_dump() for r in engine_results]
        )
        
        # Create response
        response = DetectionResponse(
            risk_score=ensemble_result['risk_score'],
            verdict=ensemble_result['verdict'],
            mode=request.mode,
            engine_results=engine_results,
            summary=ensemble_result['summary'],
            recommendations=ensemble_result['recommendations']
        )
        
        # Store analysis in database (async, don't wait)
        try:
            content_preview = request.content[:100] + '...' if len(request.content) > 100 else request.content
            history_doc = {
                'content_preview': content_preview,
                'mode': request.mode,
                'risk_score': response.risk_score,
                'verdict': response.verdict,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'engine_count': len(engine_results)
            }
            await db.analysis_history.insert_one(history_doc)
        except Exception as e:
            logger.error(f"Failed to store history: {e}")
        
        return response
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@api_router.get("/history")
async def get_history(limit: int = 20):
    """Get recent analysis history"""
    try:
        history = await db.analysis_history.find(
            {}, 
            {"_id": 0}
        ).sort("timestamp", -1).limit(limit).to_list(limit)
        
        return {"history": history, "count": len(history)}
    except Exception as e:
        logger.error(f"History retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/stats")
async def get_stats():
    """Get detection statistics"""
    try:
        total = await db.analysis_history.count_documents({})
        
        # Count by verdict
        phishing = await db.analysis_history.count_documents({"verdict": "Phishing Detected"})
        scam = await db.analysis_history.count_documents({"verdict": "Scam Detected"})
        suspicious = await db.analysis_history.count_documents({"verdict": "Suspicious"})
        safe = await db.analysis_history.count_documents({"verdict": "Safe"})
        
        return {
            "total_analyses": total,
            "verdicts": {
                "phishing": phishing,
                "scam": scam,
                "suspicious": suspicious,
                "safe": safe
            }
        }
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()