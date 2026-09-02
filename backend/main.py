from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.incident_routes import router as incident_router
from app.api.root_cause_routes import router as root_cause_router
from app.api.memory_routes import router as memory_router
from app.api.prevention_routes import router as prevention_router
from app.database.database import Base, engine

# Import all models to ensure they are registered with SQLAlchemy Base metadata
import app.models.report
import app.models.git_analysis
import app.models.incident_memory
import app.models.prevention

app = FastAPI(
    title="PostMortem-AI Incident Intelligence Engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(incident_router)
app.include_router(root_cause_router, prefix="/api")
app.include_router(memory_router, prefix="/api")
app.include_router(prevention_router, prefix="/api")

@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "PostMortem-AI Core Engine"
    }