"""AI Anomaly Detection Service."""

import json
from typing import List, Dict
import numpy as np
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session
from app.models.inspection import Inspection
from app.models.attendance import Attendance
from app.models.evidence import Evidence
from app.models.anomaly import AnomalyResult, AnomalyRiskLevel


class AnomalyDetectionService:
    """AI-powered anomaly detection."""

    # Thresholds for anomaly detection
    ATTENDANCE_THRESHOLD = 0.7  # 70% attendance
    EVIDENCE_MIN_COUNT = 3  # Minimum evidence items
    INSPECTION_FREQUENCY_DAYS = 30

    @staticmethod
    def extract_project_features(db: Session, project_id: int) -> Dict:
        """Extract features for anomaly detection."""
        # Get inspection count in last 90 days
        from datetime import datetime, timedelta
        
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        inspections = db.query(Inspection).filter(
            Inspection.project_id == project_id,
            Inspection.created_at >= ninety_days_ago
        ).all()

        # Get attendance records
        attendance_records = db.query(Attendance).filter(
            Attendance.project_id == project_id,
            Attendance.created_at >= ninety_days_ago
        ).all()

        # Get evidence collected
        evidence_records = db.query(Evidence).filter(
            Evidence.project_id == project_id,
            Evidence.created_at >= ninety_days_ago
        ).all()

        # Calculate attendance percentage
        if attendance_records:
            present_count = sum(1 for a in attendance_records if a.status.value == "PRESENT")
            attendance_percentage = (present_count / len(attendance_records)) * 100
        else:
            attendance_percentage = 0

        # Feature extraction
        features = {
            "inspection_count": len(inspections),
            "attendance_percentage": attendance_percentage,
            "evidence_count": len(evidence_records),
            "days_since_inspection": AnomalyDetectionService._days_since_last_inspection(
                inspections
            ),
            "average_evidence_per_inspection": (
                len(evidence_records) / len(inspections)
                if inspections
                else 0
            ),
        }

        return features

    @staticmethod
    def _days_since_last_inspection(inspections: List[Inspection]) -> float:
        """Calculate days since last inspection."""
        if not inspections:
            return 999
        from datetime import datetime
        
        last_inspection = max(
            inspections, key=lambda x: x.inspection_date or x.created_at
        )
        days = (
            datetime.utcnow()
            - (last_inspection.inspection_date or last_inspection.created_at)
        ).days
        return days

    @staticmethod
    def detect_anomalies(db: Session, project_id: int) -> AnomalyResult:
        """Detect anomalies using Isolation Forest."""
        features = AnomalyDetectionService.extract_project_features(db, project_id)

        # Prepare feature vector
        feature_vector = np.array(
            [
                features["inspection_count"],
                features["attendance_percentage"],
                features["evidence_count"],
                features["days_since_inspection"],
                features["average_evidence_per_inspection"],
            ]
        ).reshape(1, -1)

        # Isolation Forest model
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomaly_score = iso_forest.decision_function(feature_vector)[0]
        is_anomaly = iso_forest.predict(feature_vector)[0] == -1

        # Normalize score to 0-1 range
        normalized_score = (anomaly_score + 2) / 4  # Rough normalization
        normalized_score = max(0, min(1, normalized_score))

        # Determine risk level
        if normalized_score > 0.8:
            risk_level = AnomalyRiskLevel.CRITICAL
        elif normalized_score > 0.6:
            risk_level = AnomalyRiskLevel.HIGH
        elif normalized_score > 0.4:
            risk_level = AnomalyRiskLevel.MEDIUM
        else:
            risk_level = AnomalyRiskLevel.LOW

        # Generate reasons
        reasons = AnomalyDetectionService._generate_reasons(features)

        # Create anomaly result
        anomaly_result = AnomalyResult(
            project_id=project_id,
            anomaly_detected=1 if is_anomaly else 0,
            anomaly_score=normalized_score,
            risk_level=risk_level,
            reasons=json.dumps(reasons),
            recommendation="Human Review Required - Analysis shows unusual patterns",
        )

        db.add(anomaly_result)
        db.commit()
        db.refresh(anomaly_result)

        return anomaly_result

    @staticmethod
    def _generate_reasons(features: Dict) -> List[str]:
        """Generate human-readable reasons for anomaly."""
        reasons = []

        if features["inspection_count"] == 0:
            reasons.append("No recent inspections recorded")

        if features["attendance_percentage"] < AnomalyDetectionService.ATTENDANCE_THRESHOLD * 100:
            reasons.append(
                f"Attendance below threshold: {features['attendance_percentage']:.1f}%"
            )

        if (
            features["evidence_count"]
            < AnomalyDetectionService.EVIDENCE_MIN_COUNT
        ):
            reasons.append("Insufficient evidence collection")

        if (
            features["days_since_inspection"]
            > AnomalyDetectionService.INSPECTION_FREQUENCY_DAYS
        ):
            reasons.append(
                f"Inspection overdue: {features['days_since_inspection']:.0f} days since last inspection"
            )

        if features["average_evidence_per_inspection"] == 0:
            reasons.append("No evidence associated with inspections")

        if not reasons:
            reasons.append("Unusual pattern detected in monitoring data")

        return reasons

    @staticmethod
    def format_anomaly_response(anomaly_result: AnomalyResult) -> Dict:
        """Format anomaly result for API response."""
        reasons = json.loads(anomaly_result.reasons) if anomaly_result.reasons else []

        return {
            "anomaly_detected": bool(anomaly_result.anomaly_detected),
            "risk_level": anomaly_result.risk_level.value,
            "anomaly_score": round(anomaly_result.anomaly_score, 3),
            "reasons": reasons,
            "recommendation": anomaly_result.recommendation,
            "timestamp": anomaly_result.created_at.isoformat(),
        }
