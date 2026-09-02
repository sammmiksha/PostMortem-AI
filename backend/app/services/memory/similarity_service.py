from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.incident_memory import IncidentMemoryRecord
from app.services.memory.embedding_service import EmbeddingService

class SimilarityService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def find_similar_incidents(
        self,
        db: Session,
        query_text: str,
        service_context: Optional[str] = None,
        error_type_context: Optional[str] = None,
        exclude_incident_id: Optional[int] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Finds past incidents based on hybrid ranking:
        - Vector Similarity (70%)
        - Service Match (15%)
        - Error Type Match (15%)
        """
        records = db.query(IncidentMemoryRecord).all()
        if not records:
            return []

        query_vector = self.embedding_service.generate_embedding(query_text)
        results = []

        for rec in records:
            if exclude_incident_id and rec.incident_id == exclude_incident_id:
                continue

            rec_vec = rec.embedding or []
            v_sim = self.embedding_service.cosine_similarity(query_vector, rec_vec)

            # Bonus for service match (15%)
            s_match = 0.0
            if service_context and rec.service and service_context.lower() == rec.service.lower():
                s_match = 1.0

            # Bonus for error type match (15%)
            e_match = 0.0
            if error_type_context and rec.error_type and error_type_context.lower() in rec.error_type.lower():
                e_match = 1.0

            hybrid_score = (v_sim * 0.70) + (s_match * 0.15) + (e_match * 0.15)
            similarity_percent = round(max(0.0, min(1.0, hybrid_score)) * 100, 1)

            results.append({
                "id": rec.id,
                "incident_id": rec.incident_id,
                "summary": rec.summary,
                "root_cause": rec.root_cause,
                "resolution": rec.resolution,
                "service": rec.service or "General",
                "error_type": rec.error_type or "Unspecified",
                "similarity_score": similarity_percent,
                "created_at": str(rec.created_at)
            })

        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]
