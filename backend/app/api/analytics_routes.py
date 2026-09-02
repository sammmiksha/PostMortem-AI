from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.dependency import get_db
from app.services.analytics_service import AnalyticsService
from app.services.integrations.jira_service import JiraService
from app.services.integrations.slack_service import SlackService
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/analytics",
    tags=["Reliability Analytics & Integrations"]
)

analytics_service = AnalyticsService()
jira_service = JiraService()
slack_service = SlackService()

class JiraCreateRequest(BaseModel):
    summary: str
    description: str
    priority: Optional[str] = "High"

class SlackSendRequest(BaseModel):
    title: str
    summary: str
    root_cause: str

@router.get("/metrics")
def get_analytics_metrics(
    db: Session = Depends(get_db)
):
    return analytics_service.calculate_metrics(db)

@router.post("/jira/create-issue")
def create_jira_issue(request: JiraCreateRequest):
    payload = jira_service.create_issue_payload(
        summary=request.summary,
        description=request.description,
        priority=request.priority or "High"
    )
    return {
        "status": "success",
        "message": f"Jira Issue {payload['ticket_id']} generated successfully.",
        "payload": payload
    }

@router.post("/slack/send-alert")
def send_slack_alert(request: SlackSendRequest):
    payload = slack_service.create_block_payload(
        title=request.title,
        summary=request.summary,
        root_cause=request.root_cause
    )
    return {
        "status": "success",
        "message": "Slack Block Kit alert payload broadcast to #incidents-postmortem",
        "payload": payload
    }
