from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.database.database import Base

class IncidentReport(Base):
    __tablename__ = "incident_reports"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    incident_details = Column(Text, nullable=False)

    ai_report = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)