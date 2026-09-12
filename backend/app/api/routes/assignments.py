"""Assignment routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User, UserRole
from app.schemas.inspection import InspectionResponse
from app.services.assignment import AssignmentEngine
from app.services.project import ProjectService

router = APIRouter()


@router.post("/random")
def random_assignment(
    project_id: int = Query(...),
    scheduled_date: datetime = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Randomly assign inspection to available inspector."""
    if current_user.role not in [UserRole.ADMIN, UserRole.GOVERNMENT_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create assignments"
        )

    project = ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    try:
        inspection = AssignmentEngine.random_assignment(db, project_id, scheduled_date)
        return {
            "inspection_id": inspection.id,
            "project_id": inspection.project_id,
            "inspector_id": inspection.inspector_id,
            "scheduled_date": inspection.scheduled_date,
            "status": "PENDING",
            "method": "random",
            "message": "Inspection randomly assigned"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/risk-based")
def risk_based_assignment(
    project_id: int = Query(...),
    scheduled_date: datetime = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Assign inspection based on project risk score."""
    if current_user.role not in [UserRole.ADMIN, UserRole.GOVERNMENT_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create assignments"
        )

    project = ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    try:
        inspection = AssignmentEngine.risk_based_assignment(
            db,
            project_id,
            scheduled_date,
            project.risk_score
        )
        explanation = AssignmentEngine.get_assignment_explanation(
            project.risk_score,
            inspection.inspector_id
        )
        return {
            "inspection_id": inspection.id,
            "project_id": inspection.project_id,
            "inspector_id": inspection.inspector_id,
            "scheduled_date": inspection.scheduled_date,
            "status": "PENDING",
            "method": "risk-based",
            "project_risk_score": project.risk_score,
            "explanation": explanation,
            "message": "Inspection assigned based on risk score"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
