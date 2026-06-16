# app/schemas/analysis.py

from pydantic import BaseModel

class AnalysisResult(BaseModel):
    summary: str
    root_cause: str
    impact: str
    recommendations: list[str]