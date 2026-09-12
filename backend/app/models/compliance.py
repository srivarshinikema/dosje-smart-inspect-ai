"""Compliance model."""

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from datetime import datetime
import enum
from app.models import Base


class ComplianceItemStatus(str, enum.Enum):
    """Compliance item status."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"


class ComplianceRecord(Base):
    """Compliance record model."""

    __tablename__ = "compliance_records"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=True, index=True)
    item_name = Column(String, nullable=False)
    status = Column(Enum(ComplianceItemStatus), default=ComplianceItemStatus.PENDING, nullable=False)
    due_date = Column(DateTime, nullable=True)
    completed_date = Column(DateTime, nullable=True)
    evidence_file = Column(String, nullable=True)
    remarks = Column(Text, nullable=True)
    officer_remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ComplianceRecord {self.id}>"
