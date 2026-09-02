from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.database.database import Base

class CommitRecord(Base):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, unique=True, nullable=False, index=True)
    author = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    commit_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CommitAnalysisRecord(Base):
    __tablename__ = "commit_analysis"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, nullable=True)
    commit_hash = Column(String, nullable=False, index=True)
    confidence = Column(Integer, default=0)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
