from app.database.database import SessionLocal, Base, engine
import app.models.auth
from app.services.auth_service import AuthService
from app.services.analytics_service import AnalyticsService
from app.services.integrations.jira_service import JiraService
from app.services.integrations.slack_service import SlackService

Base.metadata.create_all(bind=engine)

auth = AuthService()
analytics = AnalyticsService()
jira = JiraService()
slack = SlackService()

print("=== 1. Testing Password Hashing & JWT Token Generation ===")
password = "SuperSecretPassword123!"
hashed = auth.hash_password(password)
verified = auth.verify_password(password, hashed)
print(f"Password Hashed: {hashed[:16]}...")
print(f"Verification Check: {verified}")

token = auth.create_token(user_id=1, email="engineer@company.com", role="Engineer")
print(f"Generated JWT Token: {token[:30]}...")

decoded = auth.decode_token(token)
print(f"Decoded JWT Payload: {decoded}")

print("\n=== 2. Testing Reliability Analytics Engine ===")
db = SessionLocal()
metrics = analytics.calculate_metrics(db)
print(f"MTTR: {metrics['mttr_minutes']} mins | MTBF: {metrics['mtbf_days']} days | Availability: {metrics['system_availability']}%")
print(f"Technical Debt Index: {metrics['technical_debt_index']}")
db.close()

print("\n=== 3. Testing Jira REST Payload Generator ===")
jira_ticket = jira.create_issue_payload(
    summary="Implement PgBouncer DB Connection Pooling",
    description="Prevent connection exhaustion during flash sale events.",
    priority="High"
)
print(f"Jira Ticket Created: {jira_ticket['ticket_id']} -> {jira_ticket['jira_url']}")

print("\n=== 4. Testing Slack Alert Payload Generator ===")
slack_alert = slack.create_block_payload(
    title="PostgreSQL Pool Exhaustion",
    summary="Unbounded db connection leak in payment checkout handler.",
    root_cause="Connection leak at payment.py line 245"
)
print(f"Slack Broadcast Channel: {slack_alert['channel']}")
print(f"Slack Blocks Count: {len(slack_alert['blocks'])}")
