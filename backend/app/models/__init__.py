"""Database models package."""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.user import User, UserRole
from app.models.project import Project, ProjectStatus, ComplianceStatus
from app.models.inspection import Inspection, InspectionStatus
from app.models.attendance import Attendance, AttendanceStatus
from app.models.evidence import Evidence
from app.models.alert import Alert, AlertType, AlertSeverity
from app.models.compliance import ComplianceRecord, ComplianceItemStatus
from app.models.risk_score import RiskScore
from app.models.anomaly import AnomalyResult, AnomalyRiskLevel
from app.models.cctv_camera import CCTVCamera, CameraStatus
from app.models.audit_log import AuditLog

__all__ = [
    "Base",
    "User",
    "UserRole",
    "Project",
    "ProjectStatus",
    "ComplianceStatus",
    "Inspection",
    "InspectionStatus",
    "Attendance",
    "AttendanceStatus",
    "Evidence",
    "Alert",
    "AlertType",
    "AlertSeverity",
    "ComplianceRecord",
    "ComplianceItemStatus",
    "RiskScore",
    "AnomalyResult",
    "AnomalyRiskLevel",
    "CCTVCamera",
    "CameraStatus",
    "AuditLog",
]
