from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database.database import Base

class GeneratedTestRecord(Base):
    __tablename__ = "generated_tests"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, nullable=True, index=True)
    test_code = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class MonitoringRuleRecord(Base):
    __tablename__ = "monitoring_rules"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, nullable=True, index=True)
    rule_text = Column(Text, nullable=False)
    platform = Column(String, default="Prometheus")
    created_at = Column(DateTime, default=datetime.utcnow)

class RunbookRecord(Base):
    __tablename__ = "runbooks"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, nullable=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ArchitectureRecommendationRecord(Base):
    __tablename__ = "architecture_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, nullable=True, index=True)
    recommendation = Column(Text, nullable=False)
    priority = Column(String, default="High")
    created_at = Column(DateTime, default=datetime.utcnow)
