from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.root_cause import RootCauseRequest, RootCauseResponse
from app.models.git_analysis import CommitAnalysisRecord, CommitRecord
from app.database.dependency import get_db
from app.services.git.commit_analyzer import CommitAnalyzer
import os

router = APIRouter(
    prefix="/root-cause",
    tags=["Root Cause Analysis"]
)

@router.post("/analyze", response_model=RootCauseResponse)
def analyze_root_cause(
    request: RootCauseRequest,
    db: Session = Depends(get_db)
):
    repo_path = request.repo_path
    if not os.path.exists(repo_path):
        # Fallback to current working directory repository if path does not exist
        repo_path = os.getcwd()

    try:
        analyzer = CommitAnalyzer(repo_path)
        result = analyzer.analyze(
            stack_trace=request.stack_trace,
            incident_summary=request.incident_summary,
            limit_output=5,
            run_ai=True
        )

        # Store top commit analysis results in DB
        for candidate in result.get("candidate_commits", []):
            analysis_rec = CommitAnalysisRecord(
                incident_id=request.incident_id,
                commit_hash=candidate.get("hash"),
                confidence=candidate.get("ai_confidence", candidate.get("score", 0)),
                explanation=candidate.get("ai_reason") or "\n".join(candidate.get("explanation", []))
            )
            db.add(analysis_rec)
        db.commit()

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Git analysis failed: {str(e)}")

@router.get("/history")
def get_root_cause_history(db: Session = Depends(get_db)):
    return db.query(CommitAnalysisRecord).order_by(CommitAnalysisRecord.created_at.desc()).limit(20).all()
