"""Inspection service."""

from sqlalchemy.orm import Session
from datetime import datetime
from app.models.inspection import Inspection, InspectionStatus
from app.schemas.inspection import InspectionCreate, InspectionUpdate


class InspectionService:
    """Inspection business logic."""

    @staticmethod
    def create_inspection(db: Session, inspection: InspectionCreate) -> Inspection:
        """Create a new inspection."""
        db_inspection = Inspection(
            **inspection.dict(),
            status=InspectionStatus.PENDING
        )
        db.add(db_inspection)
        db.commit()
        db.refresh(db_inspection)
        return db_inspection

    @staticmethod
    def get_inspection(db: Session, inspection_id: int) -> Inspection:
        """Get inspection by ID."""
        return db.query(Inspection).filter(Inspection.id == inspection_id).first()

    @staticmethod
    def list_inspections(db: Session, skip: int = 0, limit: int = 100) -> list:
        """List all inspections."""
        return db.query(Inspection).offset(skip).limit(limit).all()

    @staticmethod
    def get_project_inspections(db: Session, project_id: int) -> list:
        """Get all inspections for a project."""
        return db.query(Inspection).filter(
            Inspection.project_id == project_id
        ).order_by(Inspection.scheduled_date.desc()).all()

    @staticmethod
    def get_inspector_inspections(db: Session, inspector_id: int) -> list:
        """Get all inspections assigned to an inspector."""
        return db.query(Inspection).filter(
            Inspection.inspector_id == inspector_id
        ).order_by(Inspection.scheduled_date.desc()).all()

    @staticmethod
    def update_inspection(db: Session, inspection_id: int, inspection: InspectionUpdate) -> Inspection:
        """Update an inspection."""
        db_inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
        if db_inspection:
            update_data = inspection.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_inspection, field, value)
            if 'status' in update_data and update_data['status'] == InspectionStatus.COMPLETED:
                db_inspection.inspection_date = datetime.utcnow()
            db.commit()
            db.refresh(db_inspection)
        return db_inspection

    @staticmethod
    def get_pending_inspections(db: Session) -> list:
        """Get all pending inspections."""
        return db.query(Inspection).filter(
            Inspection.status == InspectionStatus.PENDING
        ).all()

    @staticmethod
    def get_completed_inspections(db: Session, limit: int = 10) -> list:
        """Get recently completed inspections."""
        return db.query(Inspection).filter(
            Inspection.status == InspectionStatus.COMPLETED
        ).order_by(Inspection.inspection_date.desc()).limit(limit).all()
