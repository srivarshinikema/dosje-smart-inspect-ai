"""Alerts and notifications routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User, UserRole
from app.models.alert import Alert, AlertType, AlertSeverity
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class AlertResponse(BaseModel):
    """Alert response schema."""

    id: int
    project_id: int
    alert_type: str
    severity: str
    message: str
    is_read: int
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/", response_model=list[AlertResponse])
def list_alerts(
    skip: int = 0,
    limit: int = 50,
    is_read: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List alerts (filtered by read status if specified)."""
    query = db.query(Alert)
    if is_read is not None:
        query = query.filter(Alert.is_read == is_read)
    return query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Get alert by ID."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found"
        )
    return alert


@router.post("/{alert_id}/acknowledge")
def acknowledge_alert(
    alert_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Mark alert as acknowledged."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found"
        )
    alert.is_read = 1
    alert.acknowledged_at = datetime.utcnow()
    db.commit()
    return {"message": "Alert acknowledged", "alert_id": alert_id}


@router.get("/project/{project_id}", response_model=list[AlertResponse])
def get_project_alerts(
    project_id: int,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get alerts for a specific project."""
    return (
        db.query(Alert)
        .filter(Alert.project_id == project_id)
        .order_by(Alert.created_at.desc())
        .limit(limit)
        .all()
    )


@router.get("/unread/count")
def get_unread_alert_count(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Get count of unread alerts."""
    count = db.query(Alert).filter(Alert.is_read == 0).count()
    return {"unread_alerts": count}
