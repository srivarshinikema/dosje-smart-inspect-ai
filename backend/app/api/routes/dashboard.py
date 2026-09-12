"""Dashboard routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project, ProjectStatus
from app.models.inspection import Inspection, InspectionStatus
from app.models.alert import Alert
from app.models.risk_score import RiskScore

router = APIRouter()


@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get dashboard summary for officer."""
    ninety_days_ago = datetime.utcnow() - timedelta(days=90)

    # Total projects
    total_projects = db.query(Project).count()
    active_projects = db.query(Project).filter(
        Project.status == ProjectStatus.ACTIVE
    ).count()

    # Inspections
    total_inspections = db.query(Inspection).count()
    pending_inspections = db.query(Inspection).filter(
        Inspection.status == InspectionStatus.PENDING
    ).count()
    completed_inspections = db.query(Inspection).filter(
        Inspection.status == InspectionStatus.COMPLETED,
        Inspection.inspection_date >= ninety_days_ago,
    ).count()

    # Alerts
    unread_alerts = db.query(Alert).filter(Alert.is_read == 0).count()
    recent_alerts = db.query(Alert).order_by(
        Alert.created_at.desc()
    ).limit(5).all()

    # High risk projects
    high_risk_projects = db.query(Project).filter(
        Project.risk_score >= 70.0
    ).count()

    # Average risk score
    avg_risk = db.query(Project).with_entities(
        db.func.avg(Project.risk_score)
    ).scalar() or 0

    return {
        "summary": {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "total_inspections": total_inspections,
            "pending_inspections": pending_inspections,
            "completed_inspections_90days": completed_inspections,
            "high_risk_projects": high_risk_projects,
            "average_risk_score": round(avg_risk, 2),
            "unread_alerts": unread_alerts,
        },
        "recent_alerts": [
            {
                "id": alert.id,
                "project_id": alert.project_id,
                "alert_type": alert.alert_type.value,
                "severity": alert.severity.value,
                "message": alert.message,
                "created_at": alert.created_at.isoformat(),
            }
            for alert in recent_alerts
        ],
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/project-overview")
def get_project_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed project overview."""
    projects = db.query(Project).all()

    project_data = []
    for project in projects:
        # Get recent inspection
        recent_inspection = db.query(Inspection).filter(
            Inspection.project_id == project.id
        ).order_by(Inspection.scheduled_date.desc()).first()

        project_data.append({
            "id": project.id,
            "name": project.name,
            "location": project.location,
            "latitude": project.latitude,
            "longitude": project.longitude,
            "status": project.status.value,
            "risk_score": project.risk_score,
            "compliance_status": project.compliance_status.value,
            "last_inspection_date": recent_inspection.scheduled_date.isoformat() if recent_inspection else None,
        })

    return {
        "total_projects": len(project_data),
        "projects": project_data,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/inspection-trends")
def get_inspection_trends(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get inspection trends over time."""
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    inspections = db.query(Inspection).filter(
        Inspection.created_at >= cutoff_date
    ).all()

    # Group by date
    trends = {}
    for inspection in inspections:
        date = inspection.created_at.date()
        date_str = str(date)
        if date_str not in trends:
            trends[date_str] = {"total": 0, "completed": 0, "pending": 0}
        trends[date_str]["total"] += 1
        if inspection.status == InspectionStatus.COMPLETED:
            trends[date_str]["completed"] += 1
        elif inspection.status == InspectionStatus.PENDING:
            trends[date_str]["pending"] += 1

    return {
        "trends": trends,
        "period_days": days,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/risk-distribution")
def get_risk_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get risk distribution across projects."""
    projects = db.query(Project).all()

    distribution = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
    }

    for project in projects:
        if project.risk_score >= 80:
            distribution["CRITICAL"] += 1
        elif project.risk_score >= 60:
            distribution["HIGH"] += 1
        elif project.risk_score >= 40:
            distribution["MEDIUM"] += 1
        else:
            distribution["LOW"] += 1

    return {
        "risk_distribution": distribution,
        "total_projects": len(projects),
        "timestamp": datetime.utcnow().isoformat(),
    }
