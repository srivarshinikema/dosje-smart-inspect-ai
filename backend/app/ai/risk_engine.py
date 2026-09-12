"""Risk Scoring Service."""

import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.risk_score import RiskScore
from app.models.inspection import Inspection, InspectionStatus
from app.models.attendance import Attendance, AttendanceStatus
from app.models.evidence import Evidence
from app.models.compliance import ComplianceRecord, ComplianceItemStatus


class RiskScoringEngine:
    """Risk scoring for projects."""

    # Risk weights
    WEIGHTS = {
        "attendance_risk": 0.20,
        "compliance_risk": 0.20,
        "inspection_history_risk": 0.20,
        "evidence_risk": 0.20,
        "operational_risk": 0.20,
    }

    @staticmethod
    def calculate_attendance_risk(db: Session, project_id: int) -> float:
        """Calculate attendance risk (0-100)."""
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        attendance_records = db.query(Attendance).filter(
            Attendance.project_id == project_id,
            Attendance.created_at >= ninety_days_ago,
        ).all()

        if not attendance_records:
            return 50.0  # Default medium risk

        present_count = sum(
            1 for a in attendance_records if a.status == AttendanceStatus.PRESENT
        )
        attendance_percentage = (present_count / len(attendance_records)) * 100

        # Inverse: higher attendance = lower risk
        risk = 100 - attendance_percentage
        return max(0, min(100, risk))

    @staticmethod
    def calculate_compliance_risk(db: Session, project_id: int) -> float:
        """Calculate compliance risk (0-100)."""
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        compliance_records = db.query(ComplianceRecord).filter(
            ComplianceRecord.project_id == project_id,
            ComplianceRecord.created_at >= ninety_days_ago,
        ).all()

        if not compliance_records:
            return 50.0

        non_compliant_count = sum(
            1
            for c in compliance_records
            if c.status == ComplianceItemStatus.NON_COMPLIANT
        )
        risk = (non_compliant_count / len(compliance_records)) * 100
        return max(0, min(100, risk))

    @staticmethod
    def calculate_inspection_history_risk(db: Session, project_id: int) -> float:
        """Calculate risk based on inspection frequency."""
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        inspections = db.query(Inspection).filter(
            Inspection.project_id == project_id,
            Inspection.created_at >= ninety_days_ago,
        ).all()

        # Expected: at least 3 inspections per 90 days
        expected_inspections = 3
        if len(inspections) < expected_inspections:
            risk = (1 - (len(inspections) / expected_inspections)) * 100
        else:
            risk = 0

        return max(0, min(100, risk))

    @staticmethod
    def calculate_evidence_risk(db: Session, project_id: int) -> float:
        """Calculate risk based on evidence collection."""
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        inspections = db.query(Inspection).filter(
            Inspection.project_id == project_id,
            Inspection.created_at >= ninety_days_ago,
        ).all()

        if not inspections:
            return 50.0

        total_evidence = 0
        for inspection in inspections:
            evidence = db.query(Evidence).filter(
                Evidence.inspection_id == inspection.id
            ).count()
            total_evidence += evidence

        # Expected: at least 3 evidence items per inspection
        expected_evidence = len(inspections) * 3
        if total_evidence < expected_evidence:
            risk = (1 - (total_evidence / expected_evidence)) * 100
        else:
            risk = 0

        return max(0, min(100, risk))

    @staticmethod
    def calculate_operational_risk(db: Session, project_id: int) -> float:
        """Calculate operational/general risk."""
        # Placeholder: could include facility checks, capacity, etc.
        # For now, base on inspection completion rate
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        inspections = db.query(Inspection).filter(
            Inspection.project_id == project_id,
            Inspection.created_at >= ninety_days_ago,
        ).all()

        if not inspections:
            return 40.0  # Default low-medium

        completed = sum(
            1 for i in inspections if i.status == InspectionStatus.COMPLETED
        )
        completion_rate = (completed / len(inspections)) * 100 if inspections else 0

        # Lower completion rate = higher risk
        risk = 100 - completion_rate
        return max(0, min(100, risk))

    @staticmethod
    def calculate_overall_risk(db: Session, project_id: int) -> RiskScore:
        """Calculate overall risk score using weighted average."""
        attendance_risk = RiskScoringEngine.calculate_attendance_risk(db, project_id)
        compliance_risk = RiskScoringEngine.calculate_compliance_risk(db, project_id)
        inspection_history_risk = RiskScoringEngine.calculate_inspection_history_risk(
            db, project_id
        )
        evidence_risk = RiskScoringEngine.calculate_evidence_risk(db, project_id)
        operational_risk = RiskScoringEngine.calculate_operational_risk(db, project_id)

        # Calculate weighted overall score
        overall_score = (
            attendance_risk * RiskScoringEngine.WEIGHTS["attendance_risk"]
            + compliance_risk * RiskScoringEngine.WEIGHTS["compliance_risk"]
            + inspection_history_risk
            * RiskScoringEngine.WEIGHTS["inspection_history_risk"]
            + evidence_risk * RiskScoringEngine.WEIGHTS["evidence_risk"]
            + operational_risk * RiskScoringEngine.WEIGHTS["operational_risk"]
        )

        # Generate explanation
        explanation = RiskScoringEngine._generate_explanation(
            attendance_risk,
            compliance_risk,
            inspection_history_risk,
            evidence_risk,
            operational_risk,
        )

        # Determine recommended action
        if overall_score >= 80:
            recommended_action = "Immediate investigation required"
        elif overall_score >= 60:
            recommended_action = "Urgent review and follow-up"
        elif overall_score >= 40:
            recommended_action = "Standard inspection cycle"
        else:
            recommended_action = "Routine monitoring"

        risk_score = RiskScore(
            project_id=project_id,
            overall_score=overall_score,
            attendance_risk=attendance_risk,
            compliance_risk=compliance_risk,
            inspection_history_risk=inspection_history_risk,
            evidence_risk=evidence_risk,
            operational_risk=operational_risk,
            explanation=explanation,
            recommended_action=recommended_action,
        )

        # Update project risk score
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            project.risk_score = overall_score
            db.commit()

        db.add(risk_score)
        db.commit()
        db.refresh(risk_score)

        return risk_score

    @staticmethod
    def _generate_explanation(att, comp, insp, evid, oper) -> str:
        """Generate explanation for risk factors."""
        factors = [
            (f"Attendance Risk: {att:.1f}%", att),
            (f"Compliance Risk: {comp:.1f}%", comp),
            (f"Inspection History Risk: {insp:.1f}%", insp),
            (f"Evidence Risk: {evid:.1f}%", evid),
            (f"Operational Risk: {oper:.1f}%", oper),
        ]

        # Sort by risk level (descending)
        factors.sort(key=lambda x: x[1], reverse=True)

        explanation = "Risk Factor Analysis:\n\n"
        for factor, value in factors:
            explanation += f"- {factor}\n"

        explanation += "\nInterpretation:\n"
        explanation += "The above factors contribute to the overall project risk score.\n"
        explanation += "Each factor is weighted equally (20% each) in the overall calculation.\n"
        explanation += "Higher values indicate greater risk in that category."

        return explanation

    @staticmethod
    def format_risk_response(risk_score: RiskScore) -> dict:
        """Format risk score for API response."""
        return {
            "project_id": risk_score.project_id,
            "overall_score": round(risk_score.overall_score, 2),
            "risk_level": RiskScoringEngine._get_risk_level(risk_score.overall_score),
            "factors": {
                "attendance_risk": round(risk_score.attendance_risk, 2),
                "compliance_risk": round(risk_score.compliance_risk, 2),
                "inspection_history_risk": round(risk_score.inspection_history_risk, 2),
                "evidence_risk": round(risk_score.evidence_risk, 2),
                "operational_risk": round(risk_score.operational_risk, 2),
            },
            "explanation": risk_score.explanation,
            "recommended_action": risk_score.recommended_action,
            "calculated_at": risk_score.calculated_at.isoformat(),
        }

    @staticmethod
    def _get_risk_level(score: float) -> str:
        """Determine risk level from score."""
        if score >= 80:
            return "CRITICAL"
        elif score >= 60:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        else:
            return "LOW"
