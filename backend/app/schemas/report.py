# schemas/report.py

from pydantic import BaseModel
from datetime import datetime

class ReportResponse(BaseModel):
    id: int
    title: str
    ai_report: str
    created_at: datetime

    class Config:
        from_attributes = True