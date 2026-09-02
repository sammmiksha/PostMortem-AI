from app.database.database import SessionLocal, Base, engine
import app.models.incident_memory
from app.api.memory_routes import seed_db_if_empty
from app.services.memory.similarity_service import SimilarityService
from app.services.memory.pattern_service import PatternService

# Ensure DB tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()
seed_db_if_empty(db)

similarity_service = SimilarityService()
pattern_service = PatternService()

query = "Database connection pool timeout during peak traffic"
print(f"=== Running RAG Similarity Search for Query: '{query}' ===")
results = similarity_service.find_similar_incidents(db, query, top_k=3)
for r in results:
    print(f"\n[Match {r['similarity_score']}%] Service: {r['service']} | Error: {r['error_type']}")
    print(f"  Summary: {r['summary']}")
    print(f"  Root Cause: {r['root_cause']}")
    print(f"  Resolution: {r['resolution']}")

print("\n=== Running Automated Pattern Detection ===")
patterns = pattern_service.analyze_patterns(db)
print(f"Total Incidents: {patterns['total_incidents']}")
print(f"Category Counts: {patterns['category_counts']}")
print(f"Summary: {patterns['summary']}")

db.close()
