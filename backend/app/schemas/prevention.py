from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class PreventionGenerateRequest(BaseModel):
    incident_id: Optional[int] = None
    summary: str = Field(..., min_length=5, description="Incident summary")
    root_cause: str = Field(..., min_length=5, description="Incident root cause")
    resolution: Optional[str] = ""
    category: Optional[str] = "Database"

class PreventionPackageResponse(BaseModel):
    incident_id: Optional[int] = None
    summary: str
    root_cause: str
    test_code: str
    alert_rules: str
    runbook: str
    architecture_recommendation: Dict[str, Any]
    validation_status: Dict[str, bool]
