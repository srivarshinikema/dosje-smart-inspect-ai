"""Attendance routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User, UserRole
from app.models.attendance import Attendance, AttendanceStatus
from pydantic import BaseModel

router = APIRouter()


class AttendanceCreate(BaseModel):
    """Attendance creation schema."""

    inspection_id: int
    project_id: int
    status: str  # PRESENT, ABSENT, PARTIALLY_PRESENT


class AttendanceResponse(BaseModel):
    """Attendance response schema."""

    id: int
    inspection_id: int
    project_id: int
    status: str
    recorded_at: datetime
    verified_at: datetime = None
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=AttendanceResponse)
def record_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Record attendance."""
    db_attendance = Attendance(
        inspection_id=attendance.inspection_id,
        project_id=attendance.project_id,
        status=attendance.status,
        recorded_at=datetime.utcnow(),
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance


@router.get("/inspection/{inspection_id}", response_model=list[AttendanceResponse])
def get_inspection_attendance(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get attendance records for an inspection."""
    return (
        db.query(Attendance)
        .filter(Attendance.inspection_id == inspection_id)
        .order_by(Attendance.recorded_at.desc())
        .all()
    )


@router.get("/project/{project_id}")
def get_project_attendance_percentage(
    project_id: int,
    days: int = Query(90, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get attendance percentage for project."""
    from datetime import timedelta

    cutoff_date = datetime.utcnow() - timedelta(days=days)
    attendance_records = (
        db.query(Attendance)
        .filter(
            Attendance.project_id == project_id, Attendance.recorded_at >= cutoff_date
        )
        .all()
    )

    if not attendance_records:
        return {"project_id": project_id, "attendance_percentage": 0, "total_records": 0}

    present_count = sum(
        1 for a in attendance_records if a.status == AttendanceStatus.PRESENT.value
    )
    percentage = (present_count / len(attendance_records)) * 100

    return {
        "project_id": project_id,
        "attendance_percentage": round(percentage, 2),
        "present_count": present_count,
        "total_records": len(attendance_records),
        "analysis_period_days": days,
    }
