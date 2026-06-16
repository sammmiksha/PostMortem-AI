{
  "title":"Payment Failure",
  "description":"Users cannot checkout",
  "logs":"Error logs"
}
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.incident import IncidentRequest
from app.models.report import IncidentReport
from app.database.dependency import get_db
from app.services.report_generator import ReportGenerator

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)

generator = ReportGenerator()

@router.post("/analyze")
def analyze_incident(
    request: IncidentRequest,
    db: Session = Depends(get_db)
):

    report_text = generator.generate(
        request.incident_details
    )

    report = IncidentReport(
        title=request.title,
        incident_details=request.incident_details,
        ai_report=report_text
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return {
        "id": report.id,
        "report": report.ai_report
    }


@router.get("/reports")
def get_reports(
    db: Session = Depends(get_db)
):
    return db.query(
        IncidentReport
    ).all()