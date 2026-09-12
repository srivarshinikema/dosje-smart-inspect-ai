"""Inspection model."""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Text
from datetime import datetime
import enum
from app.models import Base


class InspectionStatus(str, enum.Enum):
    """Inspection status."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Inspection(Base):
    """Inspection model."""

    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    inspector_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(Enum(InspectionStatus), default=InspectionStatus.PENDING, nullable=False)
    inspection_date = Column(DateTime, nullable=True)
    scheduled_date = Column(DateTime, nullable=False)
    gps_latitude = Column(Float, nullable=True)
    gps_longitude = Column(Float, nullable=True)
    check_in_time = Column(DateTime, nullable=True)
    check_out_time = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    observations = Column(Text, nullable=True)
    risk_score = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Inspection {self.id} - Project {self.project_id}>"
