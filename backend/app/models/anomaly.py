"""Anomaly detection result model."""

from sqlalchemy import Column, Integer, Float, DateTime, Enum, ForeignKey, Text
from datetime import datetime
import enum
from app.models import Base


class AnomalyRiskLevel(str, enum.Enum):
    """Anomaly risk level."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AnomalyResult(Base):
    """Anomaly detection result model."""

    __tablename__ = "anomaly_results"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    anomaly_detected = Column(Integer, default=0, nullable=False)
    anomaly_score = Column(Float, default=0.0, nullable=False)
    risk_level = Column(Enum(AnomalyRiskLevel), default=AnomalyRiskLevel.LOW, nullable=False)
    reasons = Column(Text, nullable=True)  # JSON list
    recommendation = Column(Text, nullable=True)
    reviewed = Column(Integer, default=0, nullable=False)
    reviewed_at = Column(DateTime, nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<AnomalyResult {self.id}>"
