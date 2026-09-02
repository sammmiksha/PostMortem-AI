import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:NewPassword123@localhost:2907/postmortem-ai"
)

try:
    engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 3})
    # Quick connectivity check
    with engine.connect() as conn:
        pass
except Exception:
    # Fallback to local SQLite database if PostgreSQL server is unreachable
    SQLITE_URL = "sqlite:///./postmortem_ai.db"
    engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()