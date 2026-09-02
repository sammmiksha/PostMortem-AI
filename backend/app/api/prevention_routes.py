from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.dependency import get_db
from app.models.prevention import (
    GeneratedTestRecord, MonitoringRuleRecord, RunbookRecord, ArchitectureRecommendationRecord
)
from app.schemas.prevention import PreventionGenerateRequest, PreventionPackageResponse
from app.services.prevention.test_generator import TestGenerator
from app.services.prevention.alert_generator import AlertGenerator
from app.services.prevention.runbook_generator import RunbookGenerator
from app.services.prevention.recommendation_engine import RecommendationEngine
from app.services.prevention.prevention_validator import PreventionValidator

router = APIRouter(
    prefix="/prevention",
    tags=["Prevention Intelligence Engine"]
)

test_gen = TestGenerator()
alert_gen = AlertGenerator()
runbook_gen = RunbookGenerator()
rec_engine = RecommendationEngine()
validator = PreventionValidator()

@router.post("/generate", response_model=PreventionPackageResponse)
def generate_prevention_package(
    request: PreventionGenerateRequest,
    db: Session = Depends(get_db)
):
    try:
        # 1. Generate artifacts
        test_code = test_gen.generate_pytest(request.summary, request.root_cause)
        alert_rules = alert_gen.generate_alerts(request.summary, request.root_cause, request.category or "Database")
        runbook = runbook_gen.generate_runbook(request.summary, request.root_cause, request.resolution or "")
        rec_data = rec_engine.generate_recommendations(request.summary, request.root_cause)

        # 2. Validate artifact quality
        package_dict = {
            "test_code": test_code,
            "alert_rules": alert_rules,
            "runbook": runbook
        }
        val_status = validator.validate_package(package_dict)

        # 3. Store in database
        db_test = GeneratedTestRecord(incident_id=request.incident_id, test_code=test_code)
        db_alert = MonitoringRuleRecord(incident_id=request.incident_id, rule_text=alert_rules)
        db_runbook = RunbookRecord(incident_id=request.incident_id, content=runbook)
        db_rec = ArchitectureRecommendationRecord(
            incident_id=request.incident_id,
            recommendation=rec_data.get("title", ""),
            priority=rec_data.get("priority", "High")
        )

        db.add(db_test)
        db.add(db_alert)
        db.add(db_runbook)
        db.add(db_rec)
        db.commit()

        return {
            "incident_id": request.incident_id,
            "summary": request.summary,
            "root_cause": request.root_cause,
            "test_code": test_code,
            "alert_rules": alert_rules,
            "runbook": runbook,
            "architecture_recommendation": rec_data,
            "validation_status": val_status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate prevention package: {str(e)}")

@router.get("/{incident_id}")
def get_prevention_package(
    incident_id: int,
    db: Session = Depends(get_db)
):
    test_rec = db.query(GeneratedTestRecord).filter(GeneratedTestRecord.incident_id == incident_id).first()
    alert_rec = db.query(MonitoringRuleRecord).filter(MonitoringRuleRecord.incident_id == incident_id).first()
    runbook_rec = db.query(RunbookRecord).filter(RunbookRecord.incident_id == incident_id).first()
    rec_record = db.query(ArchitectureRecommendationRecord).filter(ArchitectureRecommendationRecord.incident_id == incident_id).first()

    return {
        "incident_id": incident_id,
        "test_code": test_rec.test_code if test_rec else None,
        "alert_rules": alert_rec.rule_text if alert_rec else None,
        "runbook": runbook_rec.content if runbook_rec else None,
        "architecture_recommendation": rec_record.recommendation if rec_record else None
    }
