"""Project schemas."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ProjectStatus(str, Enum):
    """Project status."""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    UNDER_REVIEW = "UNDER_REVIEW"
    SUSPENDED = "SUSPENDED"


class ComplianceStatus(str, Enum):
    """Compliance status."""
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"


class ProjectCreate(BaseModel):
    """Project creation schema."""
    name: str
    institute_name: str
    scheme: str
    location: str
    latitude: float
    longitude: float
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.ACTIVE


class ProjectUpdate(BaseModel):
    """Project update schema."""
    name: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    status: Optional[ProjectStatus] = None
    compliance_status: Optional[ComplianceStatus] = None


class ProjectResponse(BaseModel):
    """Project response schema."""
    id: int
    name: str
    institute_name: str
    scheme: str
    location: str
    latitude: float
    longitude: float
    contact_person: Optional[str]
    contact_phone: Optional[str]
    contact_email: Optional[str]
    status: ProjectStatus
    risk_score: float
    compliance_status: ComplianceStatus
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
