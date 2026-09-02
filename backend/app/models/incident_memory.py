from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float
from datetime import datetime
from app.database.database import Base

class IncidentMemoryRecord(Base):
    __tablename__ = "incident_memory"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, nullable=True, index=True)
    summary = Column(Text, nullable=False)
    root_cause = Column(Text, nullable=True)
    resolution = Column(Text, nullable=True)
    service = Column(String, nullable=True, index=True)
    error_type = Column(String, nullable=True, index=True)
    embedding = Column(JSON, nullable=True)  # Stores vector as JSON array of 384 floats
    created_at = Column(DateTime, default=datetime.utcnow)

class IncidentCategoryRecord(Base):
    __tablename__ = "incident_categories"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PatternCategoryRecord(Base):
    __tablename__ = "pattern_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
