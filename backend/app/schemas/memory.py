from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class SearchMemoryRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Natural language semantic search query")
    top_k: Optional[int] = 5

class MemoryRecordResponse(BaseModel):
    id: int
    incident_id: Optional[int] = None
    summary: str
    root_cause: Optional[str] = None
    resolution: Optional[str] = None
    service: Optional[str] = "General"
    error_type: Optional[str] = "Unspecified"
    similarity_score: float
    created_at: str

class MemorySearchResponse(BaseModel):
    query: str
    results: List[MemoryRecordResponse]

class PatternResponse(BaseModel):
    total_incidents: int
    category_counts: Dict[str, int]
    patterns: List[Dict[str, Any]]
    summary: str
