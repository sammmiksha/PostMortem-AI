from fastapi import FastAPI

from app.api.incident_routes import router
from app.database.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Incident Intelligence Engine"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def health_check():
    return {
        "status": "running"
    }