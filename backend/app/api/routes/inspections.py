"""Inspection routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User, UserRole
from app.schemas.inspection import InspectionCreate, InspectionUpdate, InspectionResponse
from app.services.inspection import InspectionService

router = APIRouter()


@router.get("/", response_model=list[InspectionResponse])
def list_inspections(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all inspections."""
    return InspectionService.list_inspections(db, skip=skip, limit=limit)


@router.post("/", response_model=InspectionResponse)
def create_inspection(
    inspection: InspectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new inspection. Admin and Government Officer only."""
    if current_user.role not in [UserRole.ADMIN, UserRole.GOVERNMENT_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create inspections"
        )
    return InspectionService.create_inspection(db, inspection)


@router.get("/{inspection_id}", response_model=InspectionResponse)
def get_inspection(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get inspection by ID."""
    db_inspection = InspectionService.get_inspection(db, inspection_id)
    if not db_inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection not found"
        )
    return db_inspection


@router.put("/{inspection_id}", response_model=InspectionResponse)
def update_inspection(
    inspection_id: int,
    inspection: InspectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an inspection."""
    db_inspection = InspectionService.get_inspection(db, inspection_id)
    if not db_inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection not found"
        )
    
    # Only inspector can update their own inspection, or admin/officer can update any
    if current_user.role == UserRole.INSPECTOR and db_inspection.inspector_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this inspection"
        )
    
    return InspectionService.update_inspection(db, inspection_id, inspection)


@router.get("/project/{project_id}", response_model=list[InspectionResponse])
def get_project_inspections(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all inspections for a project."""
    return InspectionService.get_project_inspections(db, project_id)


@router.get("/inspector/{inspector_id}", response_model=list[InspectionResponse])
def get_inspector_inspections(
    inspector_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all inspections assigned to an inspector."""
    # Only inspector can view their own, or admin/officer can view any
    if current_user.role == UserRole.INSPECTOR and inspector_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these inspections"
        )
    return InspectionService.get_inspector_inspections(db, inspector_id)


@router.get("/pending/list", response_model=list[InspectionResponse])
def get_pending_inspections(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all pending inspections. Admin and Government Officer only."""
    if current_user.role not in [UserRole.ADMIN, UserRole.GOVERNMENT_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view pending inspections"
        )
    return InspectionService.get_pending_inspections(db)
