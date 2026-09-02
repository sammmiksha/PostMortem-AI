from typing import Dict, Any

class RecommendationEngine:
    def generate_recommendations(self, summary: str, root_cause: str) -> Dict[str, Any]:
        """Generates architectural recommendations and computes priority score."""
        summary_lower = summary.lower() + " " + root_cause.lower()

        if "connection" in summary_lower or "database" in summary_lower or "pool" in summary_lower:
            return {
                "priority": "Critical",
                "score": 92,
                "title": "Centralized Database Connection Pool & Proxy Middleware",
                "description": "Implement PgBouncer or a centralized database proxy middleware to manage connection pooling, enforce hard limits, and prevent connection starvation during traffic spikes.",
                "action_items": [
                    "Deploy PgBouncer instance between application workers and database primary.",
                    "Implement context-manager cleanup wrappers around all database transaction sessions.",
                    "Set hard timeout limits for idle in transaction connections."
                ]
            }

        if "auth" in summary_lower or "jwt" in summary_lower or "token" in summary_lower:
            return {
                "priority": "High",
                "score": 85,
                "title": "Distributed Cache Invalidation & Key Management",
                "description": "Implement a distributed Redis pub/sub mechanism for asynchronous JWT key rotation and cache invalidation across microservices.",
                "action_items": [
                    "Add Redis pub/sub channel for authorization key rotation events.",
                    "Implement fallback to secondary public key before raising 401 error.",
                    "Add automated token validation integration test in CI/CD pipeline."
                ]
            }

        return {
            "priority": "High",
            "score": 78,
            "title": "Asynchronous Decoupling & Circuit Breaker Pattern",
            "description": "Decouple synchronous HTTP calls to downstream dependencies using asynchronous messaging queues (RabbitMQ/Kafka) and circuit breakers (Resilience4j).",
            "action_items": [
                "Wrap downstream API calls in circuit breaker middleware.",
                "Implement exponential backoff retry logic.",
                "Add synthetic health probes for critical user journeys."
            ]
        }
