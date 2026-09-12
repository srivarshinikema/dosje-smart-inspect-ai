"""Attendance model."""

from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from datetime import datetime
import enum
from app.models import Base


class AttendanceStatus(str, enum.Enum):
    """Attendance status."""
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    PARTIALLY_PRESENT = "PARTIALLY_PRESENT"


class Attendance(Base):
    """Attendance model."""

    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.PRESENT, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Attendance {self.id}>"
