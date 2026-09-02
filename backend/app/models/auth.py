from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.database import Base

class UserRecord(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="Engineer")  # Admin, Engineer, Manager, Viewer
    created_at = Column(DateTime, default=datetime.utcnow)
