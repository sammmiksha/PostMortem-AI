from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class RootCauseRequest(BaseModel):
    stack_trace: str = Field(..., min_length=10, description="Crash traceback log")
    repo_path: str = Field(default=r"C:\projects\PostMortem-AI", description="Absolute or relative path to git repository")
    incident_summary: Optional[str] = Field(default="", description="Summary of incident context")
    incident_id: Optional[int] = Field(default=None, description="Optional incident report ID")

class CommitCandidateResponse(BaseModel):
    hash: str
    author: Optional[str] = None
    message: Optional[str] = None
    date: Optional[str] = None
    score: int
    reasons: List[str] = []
    explanation: List[str] = []
    changes_diff: List[Dict[str, Any]] = []
    ai_confidence: Optional[int] = 50
    ai_reason: Optional[str] = None
    ai_evidence: Optional[List[str]] = []
    ai_alternatives: Optional[List[str]] = []

class RootCauseResponse(BaseModel):
    stacktrace: Dict[str, Any]
    candidate_commits: List[CommitCandidateResponse]
