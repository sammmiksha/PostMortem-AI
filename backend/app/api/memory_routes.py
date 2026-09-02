from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.dependency import get_db
from app.models.incident_memory import IncidentMemoryRecord
from app.schemas.memory import SearchMemoryRequest, MemorySearchResponse, PatternResponse
from app.services.memory.similarity_service import SimilarityService
from app.services.memory.pattern_service import PatternService
from app.services.memory.embedding_service import EmbeddingService

router = APIRouter(
    prefix="/memory",
    tags=["Incident Memory & RAG"]
)

similarity_service = SimilarityService()
pattern_service = PatternService()
embedding_service = EmbeddingService()

# Seed initial knowledge base entries for demonstration / RAG search testing
SEED_INCIDENTS = [
    {
        "summary": "PostgreSQL Database Connection Pool Exhaustion during Flash Sale",
        "root_cause": "Unbounded db connection leak in payment checkout handler due to missing connection close in exception block.",
        "resolution": "Configured connection pool max_connections limit to 50, added automatic connection cleanup middleware, and enabled health monitoring.",
        "service": "Payments",
        "error_type": "ConnectionTimeoutError"
    },
    {
        "summary": "JWT Token Verification Failure across Distributed Auth Microservices",
        "root_cause": "Expired public key cache in Auth Service after secret rotation without key invalidation signal.",
        "resolution": "Implemented redis-backed public key caching with 15-minute TTL and pub/sub cache invalidation on key rotation.",
        "service": "Authentication",
        "error_type": "UnauthorizedError"
    },
    {
        "summary": "Checkout API Gateway 504 Gateway Timeout during High Traffic Spike",
        "root_cause": "Downstream inventory verification microservice blocking HTTP threads synchronously.",
        "resolution": "Refactored inventory checks to asynchronous gRPC calls with circuit breaker fallback.",
        "service": "Checkout",
        "error_type": "GatewayTimeout"
    },
    {
        "summary": "Redis Cache Eviction Storm causing Backend Database Spike",
        "root_cause": "All session cache keys configured with identical 24-hour expiration timestamp.",
        "resolution": "Added 10% random jitter to cache TTL values to smooth out eviction distribution.",
        "service": "Session",
        "error_type": "CacheMissStorm"
    },
    {
        "summary": "Database Read Replica Synchronization Lag causing Stale User Profiles",
        "root_cause": "High write volume on primary database exhausting replication thread bandwidth.",
        "resolution": "Separated heavy analytics writes to dedicated database instance.",
        "service": "User",
        "error_type": "ReplicationLagError"
    }
]

def seed_db_if_empty(db: Session):
    count = db.query(IncidentMemoryRecord).count()
    if count == 0:
        for item in SEED_INCIDENTS:
            text = f"{item['summary']} {item['root_cause']} {item['resolution']}"
            vec = embedding_service.generate_embedding(text)
            record = IncidentMemoryRecord(
                summary=item['summary'],
                root_cause=item['root_cause'],
                resolution=item['resolution'],
                service=item['service'],
                error_type=item['error_type'],
                embedding=vec
            )
            db.add(record)
        db.commit()

@router.post("/search", response_model=MemorySearchResponse)
def search_memory(
    request: SearchMemoryRequest,
    db: Session = Depends(get_db)
):
    seed_db_if_empty(db)
    results = similarity_service.find_similar_incidents(
        db=db,
        query_text=request.query,
        top_k=request.top_k or 5
    )
    return {
        "query": request.query,
        "results": results
    }

@router.get("/similar/{incident_id}")
def get_similar_incidents(
    incident_id: int,
    db: Session = Depends(get_db)
):
    seed_db_if_empty(db)
    target = db.query(IncidentMemoryRecord).filter(IncidentMemoryRecord.incident_id == incident_id).first()
    query_text = target.summary if target else "Database or system outage"

    results = similarity_service.find_similar_incidents(
        db=db,
        query_text=query_text,
        exclude_incident_id=incident_id,
        top_k=5
    )
    return {"incident_id": incident_id, "similar_incidents": results}

@router.get("/patterns", response_model=PatternResponse)
def get_incident_patterns(
    db: Session = Depends(get_db)
):
    seed_db_if_empty(db)
    return pattern_service.analyze_patterns(db)

@router.get("/stats")
def get_memory_stats(
    db: Session = Depends(get_db)
):
    seed_db_if_empty(db)
    total = db.query(IncidentMemoryRecord).count()
    patterns = pattern_service.analyze_patterns(db)
    return {
        "total_memory_records": total,
        "category_counts": patterns.get("category_counts", {}),
        "patterns_detected": len(patterns.get("patterns", []))
    }

@router.post("/seed")
def force_seed_memory(
    db: Session = Depends(get_db)
):
    seed_db_if_empty(db)
    return {"status": "seeded", "total_records": db.query(IncidentMemoryRecord).count()}
