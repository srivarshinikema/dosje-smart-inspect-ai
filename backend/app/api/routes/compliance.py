"""Compliance routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User, UserRole
from app.models.compliance import ComplianceRecord, ComplianceItemStatus
from pydantic import BaseModel

router = APIRouter()


class ComplianceCreate(BaseModel):
    """Compliance record creation schema."""

    project_id: int
    inspection_id: int = None
    item_name: str
    status: str = "PENDING"
    due_date: datetime = None
    remarks: str = None


class ComplianceUpdate(BaseModel):
    """Compliance record update schema."""

    status: str = None
    completed_date: datetime = None
    officer_remarks: str = None


class ComplianceResponse(BaseModel):
    """Compliance record response schema."""

    id: int
    project_id: int
    inspection_id: int = None
    item_name: str
    status: str
    due_date: datetime = None
    completed_date: datetime = None
    evidence_file: str = None
    remarks: str = None
    officer_remarks: str = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=ComplianceResponse)
def create_compliance_record(
    compliance: ComplianceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create compliance record."""
    if current_user.role not in [UserRole.ADMIN, UserRole.GOVERNMENT_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    db_compliance = ComplianceRecord(**compliance.dict())
    db.add(db_compliance)
    db.commit()
    db.refresh(db_compliance)
    return db_compliance


@router.get("/project/{project_id}", response_model=list[ComplianceResponse])
def get_project_compliance(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get compliance records for project."""
    return (
        db.query(ComplianceRecord)
        .filter(ComplianceRecord.project_id == project_id)
        .order_by(ComplianceRecord.created_at.desc())
        .all()
    )


@router.put("/{compliance_id}", response_model=ComplianceResponse)
def update_compliance_record(
    compliance_id: int,
    compliance: ComplianceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update compliance record."""
    if current_user.role not in [UserRole.ADMIN, UserRole.GOVERNMENT_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    db_compliance = db.query(ComplianceRecord).filter(
        ComplianceRecord.id == compliance_id
    ).first()
    if not db_compliance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compliance record not found",
        )

    update_data = compliance.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_compliance, field, value)

    db.commit()
    db.refresh(db_compliance)
    return db_compliance


@router.get("/{compliance_id}", response_model=ComplianceResponse)
def get_compliance_record(
    compliance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get compliance record by ID."""
    compliance = db.query(ComplianceRecord).filter(
        ComplianceRecord.id == compliance_id
    ).first()
    if not compliance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compliance record not found",
        )
    return compliance
