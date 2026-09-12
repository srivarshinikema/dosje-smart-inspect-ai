"""Inspection schemas."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class InspectionStatus(str, Enum):
    """Inspection status."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class InspectionCreate(BaseModel):
    """Inspection creation schema."""
    project_id: int
    inspector_id: int
    scheduled_date: datetime
    notes: Optional[str] = None


class InspectionUpdate(BaseModel):
    """Inspection update schema."""
    status: Optional[InspectionStatus] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    notes: Optional[str] = None
    observations: Optional[str] = None


class InspectionResponse(BaseModel):
    """Inspection response schema."""
    id: int
    project_id: int
    inspector_id: int
    status: InspectionStatus
    inspection_date: Optional[datetime]
    scheduled_date: datetime
    gps_latitude: Optional[float]
    gps_longitude: Optional[float]
    check_in_time: Optional[datetime]
    check_out_time: Optional[datetime]
    notes: Optional[str]
    observations: Optional[str]
    risk_score: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
