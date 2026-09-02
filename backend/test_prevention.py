from app.database.database import SessionLocal, Base, engine
import app.models.prevention
from app.services.prevention.test_generator import TestGenerator
from app.services.prevention.alert_generator import AlertGenerator
from app.services.prevention.runbook_generator import RunbookGenerator
from app.services.prevention.recommendation_engine import RecommendationEngine
from app.services.prevention.prevention_validator import PreventionValidator

Base.metadata.create_all(bind=engine)

test_gen = TestGenerator()
alert_gen = AlertGenerator()
runbook_gen = RunbookGenerator()
rec_engine = RecommendationEngine()
validator = PreventionValidator()

summary = "PostgreSQL Database Connection Pool Exhaustion during Flash Sale"
root_cause = "Unbounded connection leak in payment checkout handler due to missing session close."

print("=== 1. Generating Pytest Regression Test ===")
test_code = test_gen.generate_pytest(summary, root_cause)
print(test_code)

print("\n=== 2. Generating Prometheus Alert Rules ===")
alerts = alert_gen.generate_alerts(summary, root_cause, "Database")
print(alerts)

print("\n=== 3. Generating SRE Operational Runbook ===")
runbook = runbook_gen.generate_runbook(summary, root_cause, "Configured PgBouncer and added session cleanup context manager.")
print(runbook[:300] + "...\n")

print("=== 4. Generating Architecture Recommendations ===")
rec = rec_engine.generate_recommendations(summary, root_cause)
print(f"Priority: {rec['priority']} (Score: {rec['score']})")
print(f"Title: {rec['title']}")

print("\n=== 5. Running Prevention Quality Validator ===")
pkg = {"test_code": test_code, "alert_rules": alerts, "runbook": runbook}
val = validator.validate_package(pkg)
print(f"Validation Results: {val}")
