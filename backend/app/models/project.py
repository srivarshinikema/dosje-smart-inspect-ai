"""Project model."""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from datetime import datetime
import enum
from app.models import Base


class ProjectStatus(str, enum.Enum):
    """Project status."""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    UNDER_REVIEW = "UNDER_REVIEW"
    SUSPENDED = "SUSPENDED"


class ComplianceStatus(str, enum.Enum):
    """Compliance status."""
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"


class Project(Base):
    """Project model."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    institute_name = Column(String, nullable=False)
    scheme = Column(String, nullable=False)
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    contact_person = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.ACTIVE, nullable=False)
    risk_score = Column(Float, default=0.0, nullable=False)
    compliance_status = Column(Enum(ComplianceStatus), default=ComplianceStatus.PENDING, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Project {self.name}>"
