class RunbookGenerator:
    def generate_runbook(self, summary: str, root_cause: str, resolution: str = "") -> str:
        """Generates a structured SRE operational runbook in markdown."""
        return f"""# SRE Incident Runbook: {summary}

## 1. Symptoms & Detection
* **Primary Alert**: High error rate, elevated latency, or connection timeout alerts.
* **User Impact**: API request timeouts, HTTP 500/504 errors, degraded user checkout experience.
* **Observability Dashboards**: Grafana -> System Metrics -> DB Pool & Latency panels.

## 2. Diagnosis & Triage
1. Check service health status endpoint (`GET /health`).
2. Inspect application container logs for exception tracebacks matching `{root_cause[:60]}...`.
3. Check active connection metrics and thread pool saturation.

## 3. Immediate Resolution & Remediation
1. **Restart Non-responsive Worker Nodes**:
   `kubectl rollout restart deployment/service-backend`
2. **Flush / Increase Connection Limits**:
   If connection pool exhaustion is detected, temporarily scale replica instances to distribute load.
3. **Apply Emergency Circuit Breaker**:
   Enable fallback response mode if downstream dependency is unresponsive.

## 4. Root Cause Verification & Resolution Steps
* Verify that connection resources are freed after request lifecycle completion.
* Check post-incident resolution steps: {resolution or "Apply permanent code fix and update connection pool timeouts."}

## 5. Escalation Path
* **L1 On-Call SRE**: Re-route traffic, restart deployment pods.
* **Database Administrator (DBA)**: Inspect active database locks & connection processes (`pg_stat_activity`).
* **Lead Engineer**: Approve emergency hotfix PR and release rollback if needed.
"""
