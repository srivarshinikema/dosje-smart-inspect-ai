"""CCTV camera routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User, UserRole
from app.models.cctv_camera import CCTVCamera, CameraStatus
from pydantic import BaseModel

router = APIRouter()


class CCTVCameraCreate(BaseModel):
    """CCTV camera creation schema."""

    project_id: int
    camera_id: str
    name: str
    location: str
    rtsp_url: str = None
    is_demo: bool = True


class CCTVCameraResponse(BaseModel):
    """CCTV camera response schema."""

    id: int
    project_id: int
    camera_id: str
    name: str
    location: str
    rtsp_url: str = None
    is_demo: bool
    status: str
    last_active: datetime = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=CCTVCameraResponse)
def create_camera(
    camera: CCTVCameraCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create CCTV camera."""
    if current_user.role not in [UserRole.ADMIN, UserRole.GOVERNMENT_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    db_camera = CCTVCamera(**camera.dict())
    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    return db_camera


@router.get("/project/{project_id}", response_model=list[CCTVCameraResponse])
def get_project_cameras(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get CCTV cameras for project."""
    return db.query(CCTVCamera).filter(
        CCTVCamera.project_id == project_id
    ).all()


@router.get("/{camera_id}", response_model=CCTVCameraResponse)
def get_camera(
    camera_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get camera by ID."""
    camera = db.query(CCTVCamera).filter(
        CCTVCamera.camera_id == camera_id
    ).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found",
        )
    return camera


@router.get("/")
def list_cameras(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all cameras."""
    return db.query(CCTVCamera).offset(skip).limit(limit).all()
