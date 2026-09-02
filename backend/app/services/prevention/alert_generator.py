class AlertGenerator:
    def generate_alerts(self, summary: str, root_cause: str, category: str = "Database") -> str:
        """Generates Prometheus monitoring alert rules based on incident domain."""
        cat_lower = category.lower()

        if "database" in cat_lower or "postgres" in summary.lower() or "pool" in root_cause.lower():
            return """# Prometheus Alert Rules: Database Operational Health
groups:
  - name: postmortem_database_alerts
    rules:
      - alert: DatabaseConnectionPoolExhaustion
        expr: pg_stat_activity_count / pg_max_connections > 0.80
        for: 2m
        labels:
          severity: critical
          team: sre
        annotations:
          summary: "Database connection pool utilization exceeded 80%"
          description: "Active connections on {{ $labels.instance }} reached {{ $value | humanizePercentage }}. Risk of connection leak or pool starvation."

      - alert: HighDatabaseQueryLatency
        expr: histogram_quantile(0.95, rate(pg_stat_database_xact_commit_duration_seconds_bucket[5m])) > 1.5
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "95th percentile DB latency > 1.5s"
"""

        if "auth" in cat_lower or "jwt" in summary.lower() or "token" in root_cause.lower():
            return """# Prometheus Alert Rules: Authentication & Security
groups:
  - name: postmortem_auth_alerts
    rules:
      - alert: HighAuthFailureRate
        expr: rate(http_requests_total{status=~"401|403"}[5m]) / rate(http_requests_total[5m]) > 0.10
        for: 2m
        labels:
          severity: critical
          team: security
        annotations:
          summary: "Authentication failure rate exceeded 10%"
          description: "Potential credential stuffing, expired token storm, or auth key rotation failure."
"""

        return """# Prometheus Alert Rules: General System Resilience
groups:
  - name: postmortem_system_alerts
    rules:
      - alert: HighHttp5xxErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "HTTP 5xx Error Rate > 5%"
          description: "High error rate detected across service endpoints."

      - alert: HighP99Latency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 2.0
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "P99 HTTP Latency exceeded 2 seconds"
"""
