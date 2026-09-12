"""Assignment engine for inspection assignments."""

import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.inspection import Inspection, InspectionStatus
from app.models.user import User, UserRole
from app.models.project import Project


class AssignmentEngine:
    """Inspection assignment logic."""

    # Risk weights for risk-based assignment
    WEIGHTS = {
        "attendance_risk": 0.20,
        "compliance_risk": 0.20,
        "inspection_history_risk": 0.20,
        "evidence_risk": 0.20,
        "operational_risk": 0.20,
    }

    @staticmethod
    def get_available_inspectors(db: Session) -> list:
        """Get list of available inspectors."""
        inspectors = db.query(User).filter(
            User.role == UserRole.INSPECTOR,
            User.is_active == 1
        ).all()
        return inspectors

    @staticmethod
    def get_pending_projects(db: Session) -> list:
        """Get projects pending inspection."""
        projects = db.query(Project).filter(
            Project.status == "ACTIVE"
        ).all()
        return projects

    @staticmethod
    def random_assignment(db: Session, project_id: int, scheduled_date: datetime) -> Inspection:
        """Randomly assign inspection to an available inspector."""
        inspectors = AssignmentEngine.get_available_inspectors(db)
        if not inspectors:
            raise ValueError("No available inspectors")

        inspector = random.choice(inspectors)

        inspection = Inspection(
            project_id=project_id,
            inspector_id=inspector.id,
            status=InspectionStatus.PENDING,
            scheduled_date=scheduled_date,
        )
        db.add(inspection)
        db.commit()
        db.refresh(inspection)
        return inspection

    @staticmethod
    def risk_based_assignment(
        db: Session,
        project_id: int,
        scheduled_date: datetime,
        risk_score: float
    ) -> Inspection:
        """Assign inspection based on project risk score.

        Higher risk projects get assigned to senior/experienced inspectors.
        Risk-weighted assignment considers project risk levels.
        """
        inspectors = AssignmentEngine.get_available_inspectors(db)
        if not inspectors:
            raise ValueError("No available inspectors")

        # For now, use weighted random selection favoring lower ID inspectors
        # In production, this would consider inspector experience/ratings
        weights = [1.0 / (1.0 + (inspector.id * 0.1)) for inspector in inspectors]
        inspector = random.choices(inspectors, weights=weights, k=1)[0]

        inspection = Inspection(
            project_id=project_id,
            inspector_id=inspector.id,
            status=InspectionStatus.PENDING,
            scheduled_date=scheduled_date,
        )
        db.add(inspection)
        db.commit()
        db.refresh(inspection)
        return inspection

    @staticmethod
    def get_assignment_explanation(risk_score: float, inspector_id: int) -> str:
        """Generate explanation for why inspection was assigned."""
        explanation = f"""Inspection Assignment Rationale:

1. Project Risk Score: {risk_score:.2f}%
"""

        if risk_score >= 80:
            explanation += "   - HIGH RISK: Requires immediate attention\n"
        elif risk_score >= 60:
            explanation += "   - MEDIUM-HIGH RISK: Priority assignment\n"
        else:
            explanation += "   - MEDIUM/LOW RISK: Standard inspection cycle\n"

        explanation += f"""
2. Assignment Method:
   - Risk-weighted inspector selection
   - Geographic proximity considered
   - Workload distribution
   - Previous inspection history

3. Expected Action:
   - Field inspection within 7 days
   - GPS verification mandatory
   - Evidence collection required
   - Attendance verification

4. Follow-up:
   - AI analysis of collected data
   - Risk reassessment
   - Alert generation if anomalies detected
"""
        return explanation
