"""AI routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User, UserRole
from app.ai.anomaly import AnomalyDetectionService
from app.ai.risk_engine import RiskScoringEngine
from app.services.project import ProjectService

router = APIRouter()


@router.post("/analyze/{project_id}")
def analyze_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Analyze project for anomalies and risks."""
    if current_user.role not in [UserRole.ADMIN, UserRole.GOVERNMENT_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to analyze projects",
        )

    project = ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    # Detect anomalies
    anomaly_result = AnomalyDetectionService.detect_anomalies(db, project_id)
    anomaly_response = AnomalyDetectionService.format_anomaly_response(anomaly_result)

    # Calculate risk score
    risk_score = RiskScoringEngine.calculate_overall_risk(db, project_id)
    risk_response = RiskScoringEngine.format_risk_response(risk_score)

    return {
        "project_id": project_id,
        "anomaly_analysis": anomaly_response,
        "risk_analysis": risk_response,
        "timestamp": anomaly_result.created_at.isoformat(),
        "note": "Analysis Result: Human Review Required. AI assists but does not make final determinations.",
    }


@router.get("/risk/{project_id}")
def get_project_risk(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get latest risk score for project."""
    from app.models.risk_score import RiskScore

    risk_score = db.query(RiskScore).filter(
        RiskScore.project_id == project_id
    ).order_by(RiskScore.calculated_at.desc()).first()

    if not risk_score:
        # Calculate if not available
        risk_score = RiskScoringEngine.calculate_overall_risk(db, project_id)

    return RiskScoringEngine.format_risk_response(risk_score)


@router.get("/anomalies/{project_id}")
def get_project_anomalies(
    project_id: int,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get recent anomaly detections for project."""
    from app.models.anomaly import AnomalyResult

    anomalies = db.query(AnomalyResult).filter(
        AnomalyResult.project_id == project_id
    ).order_by(AnomalyResult.created_at.desc()).limit(limit).all()

    return [
        AnomalyDetectionService.format_anomaly_response(anomaly)
        for anomaly in anomalies
    ]
