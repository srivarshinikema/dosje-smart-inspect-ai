"""Evidence routes."""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
import os
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.evidence import Evidence
from pydantic import BaseModel

router = APIRouter()

UPLOAD_DIR = "uploads/evidence"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class EvidenceCreate(BaseModel):
    """Evidence creation schema."""

    inspection_id: int
    project_id: int
    file_type: str  # image, video, document
    gps_latitude: float = None
    gps_longitude: float = None
    description: str = None
    captured_at: datetime


class EvidenceResponse(BaseModel):
    """Evidence response schema."""

    id: int
    inspection_id: int
    project_id: int
    inspector_id: int
    file_path: str
    file_type: str
    gps_latitude: float = None
    gps_longitude: float = None
    description: str = None
    captured_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=EvidenceResponse)
async def upload_evidence(
    inspection_id: int,
    project_id: int,
    file_type: str,
    file: UploadFile = File(...),
    gps_latitude: float = None,
    gps_longitude: float = None,
    description: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Upload evidence file."""
    # Save file
    file_location = f"{UPLOAD_DIR}/{inspection_id}_{datetime.utcnow().timestamp()}_{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    # Create evidence record
    evidence = Evidence(
        inspection_id=inspection_id,
        project_id=project_id,
        inspector_id=current_user.id,
        file_path=file_location,
        file_type=file_type,
        gps_latitude=gps_latitude,
        gps_longitude=gps_longitude,
        description=description,
        captured_at=datetime.utcnow(),
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    return evidence


@router.get("/inspection/{inspection_id}", response_model=list[EvidenceResponse])
def get_inspection_evidence(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all evidence for an inspection."""
    return db.query(Evidence).filter(Evidence.inspection_id == inspection_id).all()


@router.get("/project/{project_id}", response_model=list[EvidenceResponse])
def get_project_evidence(
    project_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all evidence for a project."""
    return (
        db.query(Evidence)
        .filter(Evidence.project_id == project_id)
        .order_by(Evidence.captured_at.desc())
        .limit(limit)
        .all()
    )


@router.delete("/{evidence_id}")
def delete_evidence(
    evidence_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete evidence."""
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Evidence not found"
        )
    db.delete(evidence)
    db.commit()
    return {"message": "Evidence deleted"}
