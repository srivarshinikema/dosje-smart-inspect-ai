"""Risk score model."""

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Text
from datetime import datetime
from app.models import Base


class RiskScore(Base):
    """Risk score model."""

    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    overall_score = Column(Float, default=0.0, nullable=False)
    attendance_risk = Column(Float, default=0.0, nullable=False)
    compliance_risk = Column(Float, default=0.0, nullable=False)
    inspection_history_risk = Column(Float, default=0.0, nullable=False)
    evidence_risk = Column(Float, default=0.0, nullable=False)
    operational_risk = Column(Float, default=0.0, nullable=False)
    explanation = Column(Text, nullable=True)
    recommended_action = Column(Text, nullable=True)
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<RiskScore {self.id} - Project {self.project_id}>"
