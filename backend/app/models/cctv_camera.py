"""CCTV Camera model."""

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Boolean
from datetime import datetime
import enum
from app.models import Base


class CameraStatus(str, enum.Enum):
    """Camera status."""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    MAINTENANCE = "MAINTENANCE"


class CCTVCamera(Base):
    """CCTV Camera model."""

    __tablename__ = "cctv_cameras"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    camera_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    rtsp_url = Column(String, nullable=True)
    is_demo = Column(Boolean, default=True, nullable=False)  # Mark if simulated
    status = Column(Enum(CameraStatus), default=CameraStatus.ACTIVE, nullable=False)
    last_active = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<CCTVCamera {self.camera_id}>"
