from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.incident_memory import IncidentMemoryRecord, IncidentCategoryRecord
from app.services.llm_service import LLMService
import re

CATEGORIES = [
    "Database", "Authentication", "Networking", "Configuration",
    "Caching", "API", "Infrastructure", "Security"
]

CATEGORY_KEYWORDS = {
    "Database": ["database", "postgres", "sql", "query", "connection pool", "deadlock", "db"],
    "Authentication": ["auth", "jwt", "token", "login", "unauthorized", "password", "session"],
    "Networking": ["timeout", "socket", "http", "latency", "dns", "connection", "gateway"],
    "Configuration": ["config", "env", "setting", "misconfiguration", "variable", "yaml"],
    "Caching": ["cache", "redis", "memcached", "eviction", "hit rate"],
    "API": ["endpoint", "route", "graphql", "rest", "payload", "rate limit"],
    "Infrastructure": ["memory", "cpu", "disk", "oom", "node", "pod", "docker"],
    "Security": ["cors", "vulnerability", "xss", "permission", "access denied"]
}

class PatternService:
    def __init__(self):
        self.llm = LLMService()

    def categorize_incident(self, text: str) -> str:
        """Determines category based on text keyword matching."""
        text_lower = text.lower()
        for cat, words in CATEGORY_KEYWORDS.items():
            for w in words:
                if re.search(r'\b' + re.escape(w) + r'\b', text_lower):
                    return cat
        return "General"

    def analyze_patterns(self, db: Session) -> Dict[str, Any]:
        """Scans incident memory, groups by category, and detects recurring patterns."""
        records = db.query(IncidentMemoryRecord).all()
        if not records:
            return {
                "total_incidents": 0,
                "category_counts": {},
                "patterns": [],
                "recommendation": "No incident memory data available to analyze patterns."
            }

        counts = {c: 0 for c in CATEGORIES}
        counts["General"] = 0
        cat_incidents = {}

        for rec in records:
            cat = self.categorize_incident(f"{rec.summary} {rec.root_cause or ''}")
            counts[cat] = counts.get(cat, 0) + 1
            if cat not in cat_incidents:
                cat_incidents[cat] = []
            cat_incidents[cat].append(rec.summary)

        # Identify top failing categories (threshold >= 2 incidents)
        recurring_patterns = []
        for cat, count in counts.items():
            if count >= 2:
                recurring_patterns.append({
                    "category": cat,
                    "count": count,
                    "sample_incidents": cat_incidents.get(cat, [])[:3],
                    "risk_level": "High" if count >= 3 else "Medium"
                })

        return {
            "total_incidents": len(records),
            "category_counts": counts,
            "patterns": recurring_patterns,
            "summary": f"Detected {len(recurring_patterns)} recurring failure patterns across {len(records)} recorded incidents."
        }
