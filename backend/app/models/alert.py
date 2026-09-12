"""Alert model."""

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from datetime import datetime
import enum
from app.models import Base


class AlertType(str, enum.Enum):
    """Alert type."""
    HIGH_RISK = "HIGH_RISK"
    ANOMALY_DETECTED = "ANOMALY_DETECTED"
    MISSING_EVIDENCE = "MISSING_EVIDENCE"
    LOW_ATTENDANCE = "LOW_ATTENDANCE"
    COMPLIANCE_ISSUE = "COMPLIANCE_ISSUE"
    PENDING_INSPECTION = "PENDING_INSPECTION"


class AlertSeverity(str, enum.Enum):
    """Alert severity."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Alert(Base):
    """Alert model."""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    alert_type = Column(Enum(AlertType), nullable=False)
    severity = Column(Enum(AlertSeverity), default=AlertSeverity.MEDIUM, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    acknowledged_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Alert {self.id} - {self.alert_type}>"
