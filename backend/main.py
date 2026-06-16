from fastapi import FastAPI

from app.api.incident_routes import router
from app.database.database import Base, engine

app = FastAPI(
    title="Incident Intelligence Engine"
)

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def health_check():
    return {
        "status": "running"
    }