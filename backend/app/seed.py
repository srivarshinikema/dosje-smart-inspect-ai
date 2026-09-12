"""Database seed script for demo data."""

import sys
from datetime import datetime, timedelta
import random
import json

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import Base
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
from app.core.security import hash_password


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created/verified")


def seed_users(db: Session):
    """Create demo users."""
    # Check if users already exist
    admin = db.query(User).filter(User.email == "admin@demo.com").first()
    if admin:
        print("✓ Demo users already exist, skipping...")
        return

    # Create users
    users_data = [
        {
            "email": "admin@demo.com",
            "username": "admin_user",
            "full_name": "Admin User",
            "password": "admin123",
            "role": UserRole.ADMIN,
        },
        {
            "email": "officer@demo.com",
            "username": "govt_officer",
            "full_name": "Government Officer",
            "password": "officer123",
            "role": UserRole.GOVERNMENT_OFFICER,
        },
        {
            "email": "inspector1@demo.com",
            "username": "inspector_one",
            "full_name": "Inspector One",
            "password": "inspector123",
            "role": UserRole.INSPECTOR,
        },
        {
            "email": "inspector2@demo.com",
            "username": "inspector_two",
            "full_name": "Inspector Two",
            "password": "inspector123",
            "role": UserRole.INSPECTOR,
        },
        {
            "email": "representative@demo.com",
            "username": "project_rep",
            "full_name": "Project Representative",
            "password": "project123",
            "role": UserRole.PROJECT_REPRESENTATIVE,
        },
    ]

    for user_data in users_data:
        password = user_data.pop("password")
        user = User(
            **user_data,
            hashed_password=hash_password(password),
            is_active=1,
        )
        db.add(user)

    db.commit()
    print(f"✓ Created {len(users_data)} demo users")


def seed_projects(db: Session):
    """Create demo projects."""
    # Check if projects already exist
    existing = db.query(Project).first()
    if existing:
        print("✓ Demo projects already exist, skipping...")
        return

    institutes = [
        "Rajendra Institute of Social Development",
        "National Center for Community Health",
        "DoSJE Training Academy",
        "Women Empowerment Foundation",
        "Youth Development Council",
        "Tribal Welfare Organization",
        "Disability Support Center",
        "Education Access Initiative",
        "Healthcare Services Network",
        "Skill Development Bureau",
    ]

    schemes = [
        "Pradhan Mantri Kaushal Vikas Yojana",
        "Integrated Child Development Services",
        "National Social Assistance Programme",
        "Scholarship for Girl Child",
        "Tribal Development Program",
        "Disability Rehabilitation Scheme",
        "Women Safety Initiative",
        "Community Health Program",
        "Rural Education Scheme",
        "Youth Entrepreneurship Program",
    ]

    locations = [
        ("Delhi", 28.7041, 77.1025),
        ("Mumbai", 19.0760, 72.8777),
        ("Bangalore", 12.9716, 77.5946),
        ("Hyderabad", 17.3850, 78.4867),
        ("Pune", 18.5204, 73.8567),
        ("Chennai", 13.0827, 80.2707),
        ("Kolkata", 22.5726, 88.3639),
        ("Ahmedabad", 23.0225, 72.5714),
        ("Lucknow", 26.8467, 80.9462),
        ("Jaipur", 26.9124, 75.7873),
    ]

    projects = []
    for i in range(10):
        location_name, lat, lon = locations[i]
        project = Project(
            name=f"Project {i+1}: {schemes[i].split()[0]}",
            institute_name=institutes[i],
            scheme=schemes[i],
            location=location_name,
            latitude=lat + random.uniform(-0.5, 0.5),
            longitude=lon + random.uniform(-0.5, 0.5),
            contact_person=f"Contact Person {i+1}",
            contact_phone=f"+91-98000{1000+i}",
            contact_email=f"project{i+1}@institute.gov.in",
            status=random.choice([ProjectStatus.ACTIVE, ProjectStatus.ACTIVE]),
            risk_score=random.uniform(20, 85),
            compliance_status=random.choice([
                ComplianceStatus.PENDING,
                ComplianceStatus.IN_PROGRESS,
                ComplianceStatus.COMPLIANT,
            ]),
            description=f"Demo project for {institutes[i]}. [SYNTHETIC DATA]",
        )
        projects.append(project)
        db.add(project)

    db.commit()
    print(f"✓ Created {len(projects)} demo projects")


def seed_inspections(db: Session):
    """Create demo inspections."""
    existing = db.query(Inspection).first()
    if existing:
        print("✓ Demo inspections already exist, skipping...")
        return

    projects = db.query(Project).all()
    inspectors = db.query(User).filter(
        User.role == UserRole.INSPECTOR
    ).all()

    if not projects or not inspectors:
        print("✗ Projects or inspectors not found")
        return

    inspections = []
    for i in range(30):
        project = random.choice(projects)
        inspector = random.choice(inspectors)
        scheduled_date = datetime.utcnow() + timedelta(days=random.randint(-30, 30))
        inspection = Inspection(
            project_id=project.id,
            inspector_id=inspector.id,
            status=random.choice([
                InspectionStatus.PENDING,
                InspectionStatus.IN_PROGRESS,
                InspectionStatus.COMPLETED,
            ]),
            scheduled_date=scheduled_date,
            inspection_date=scheduled_date if random.random() > 0.4 else None,
            gps_latitude=project.latitude + random.uniform(-0.01, 0.01),
            gps_longitude=project.longitude + random.uniform(-0.01, 0.01),
            notes=f"Demo inspection note {i+1}",
            observations=f"Observations recorded during inspection",
            risk_score=random.uniform(20, 90),
        )
        inspections.append(inspection)
        db.add(inspection)

    db.commit()
    print(f"✓ Created {len(inspections)} demo inspections")


def seed_attendance(db: Session):
    """Create demo attendance records."""
    existing = db.query(Attendance).first()
    if existing:
        print("✓ Demo attendance records already exist, skipping...")
        return

    inspections = db.query(Inspection).all()
    projects = db.query(Project).all()

    if not inspections or not projects:
        return

    attendance_records = []
    for inspection in inspections:
        # 1-3 attendance records per inspection
        for _ in range(random.randint(1, 3)):
            record = Attendance(
                inspection_id=inspection.id,
                project_id=inspection.project_id,
                status=random.choice([
                    AttendanceStatus.PRESENT,
                    AttendanceStatus.PRESENT,
                    AttendanceStatus.ABSENT,
                    AttendanceStatus.PARTIALLY_PRESENT,
                ]),
            )
            attendance_records.append(record)
            db.add(record)

    db.commit()
    print(f"✓ Created {len(attendance_records)} demo attendance records")


def seed_alerts(db: Session):
    """Create demo alerts."""
    existing = db.query(Alert).first()
    if existing:
        print("✓ Demo alerts already exist, skipping...")
        return

    projects = db.query(Project).all()
    if not projects:
        return

    alerts = []
    for project in projects:
        for _ in range(random.randint(1, 3)):
            alert = Alert(
                project_id=project.id,
                alert_type=random.choice([
                    AlertType.HIGH_RISK,
                    AlertType.ANOMALY_DETECTED,
                    AlertType.MISSING_EVIDENCE,
                    AlertType.LOW_ATTENDANCE,
                    AlertType.COMPLIANCE_ISSUE,
                ]),
                severity=random.choice([
                    AlertSeverity.LOW,
                    AlertSeverity.MEDIUM,
                    AlertSeverity.HIGH,
                    AlertSeverity.CRITICAL,
                ]),
                message="Demo alert message - synthetic data for testing",
                is_read=random.choice([0, 0, 1]),
            )
            alerts.append(alert)
            db.add(alert)

    db.commit()
    print(f"✓ Created {len(alerts)} demo alerts")


def seed_risk_scores(db: Session):
    """Create demo risk scores."""
    existing = db.query(RiskScore).first()
    if existing:
        print("✓ Demo risk scores already exist, skipping...")
        return

    projects = db.query(Project).all()
    if not projects:
        return

    risk_scores = []
    for project in projects:
        score = RiskScore(
            project_id=project.id,
            overall_score=project.risk_score,
            attendance_risk=random.uniform(10, 100),
            compliance_risk=random.uniform(10, 100),
            inspection_history_risk=random.uniform(10, 100),
            evidence_risk=random.uniform(10, 100),
            operational_risk=random.uniform(10, 100),
            explanation="Risk factors calculated from recent inspection data and project history.",
            recommended_action="Standard monitoring" if project.risk_score < 60 else "Urgent review required",
        )
        risk_scores.append(score)
        db.add(score)

    db.commit()
    print(f"✓ Created {len(risk_scores)} demo risk scores")


def seed_anomaly_results(db: Session):
    """Create demo anomaly detection results."""
    existing = db.query(AnomalyResult).first()
    if existing:
        print("✓ Demo anomaly results already exist, skipping...")
        return

    projects = db.query(Project).all()
    if not projects:
        return

    anomalies = []
    for project in projects:
        reasons = [
            "Unusual attendance pattern",
            "Missing evidence items",
            "Inspection frequency anomaly",
            "Compliance deviation",
        ]
        anomaly = AnomalyResult(
            project_id=project.id,
            anomaly_detected=1 if project.risk_score > 70 else 0,
            anomaly_score=project.risk_score / 100,
            risk_level=AnomalyRiskLevel.CRITICAL if project.risk_score > 80 else (
                AnomalyRiskLevel.HIGH if project.risk_score > 60 else AnomalyRiskLevel.MEDIUM
            ),
            reasons=json.dumps(random.sample(reasons, k=random.randint(1, 2))),
            recommendation="Human Review Required - Anomaly detected in monitoring data",
            reviewed=random.choice([0, 1]),
        )
        anomalies.append(anomaly)
        db.add(anomaly)

    db.commit()
    print(f"✓ Created {len(anomalies)} demo anomaly results")


def seed_cctv_cameras(db: Session):
    """Create demo CCTV cameras."""
    existing = db.query(CCTVCamera).first()
    if existing:
        print("✓ Demo CCTV cameras already exist, skipping...")
        return

    projects = db.query(Project).all()
    if not projects:
        return

    cameras = []
    for project in projects:
        for cam_num in range(random.randint(1, 3)):
            camera = CCTVCamera(
                project_id=project.id,
                camera_id=f"CAM-{project.id}-{cam_num}",
                name=f"Demo Camera {cam_num} - {project.name}",
                location=f"Location {cam_num} at {project.location}",
                rtsp_url=None,  # No real RTSP URL
                is_demo=True,  # Mark as demo/simulated
                status=CameraStatus.ACTIVE,
            )
            cameras.append(camera)
            db.add(camera)

    db.commit()
    print(f"✓ Created {len(cameras)} demo CCTV cameras (simulated)")


def seed_compliance_records(db: Session):
    """Create demo compliance records."""
    existing = db.query(ComplianceRecord).first()
    if existing:
        print("✓ Demo compliance records already exist, skipping...")
        return

    projects = db.query(Project).all()
    inspections = db.query(Inspection).all()

    if not projects:
        return

    compliance_items = [
        "Document verification",
        "Facility inspection",
        "Staff verification",
        "Beneficiary enrollment",
        "Financial audit",
        "Program delivery assessment",
    ]

    records = []
    for project in projects:
        for item in compliance_items:
            inspection = random.choice(inspections) if inspections else None
            record = ComplianceRecord(
                project_id=project.id,
                inspection_id=inspection.id if inspection else None,
                item_name=item,
                status=random.choice([
                    ComplianceItemStatus.PENDING,
                    ComplianceItemStatus.IN_PROGRESS,
                    ComplianceItemStatus.COMPLIANT,
                    ComplianceItemStatus.NON_COMPLIANT,
                ]),
                due_date=datetime.utcnow() + timedelta(days=random.randint(1, 60)),
                remarks="Demo compliance remarks",
            )
            records.append(record)
            db.add(record)

    db.commit()
    print(f"✓ Created {len(records)} demo compliance records")


def seed_database():
    """Run all seed functions."""
    print("\n" + "="*60)
    print("DoSJE SmartInspect AI - Database Seed Script")
    print("="*60)
    print("\nSeeding database with synthetic demo data...\n")

    db = SessionLocal()
    try:
        init_db()
        seed_users(db)
        seed_projects(db)
        seed_inspections(db)
        seed_attendance(db)
        seed_alerts(db)
        seed_risk_scores(db)
        seed_anomaly_results(db)
        seed_cctv_cameras(db)
        seed_compliance_records(db)

        print("\n" + "="*60)
        print("✓ Database seeding completed successfully!")
        print("="*60)
        print("\nDemo Login Credentials:")
        print("-" * 60)
        print("Admin:                  admin@demo.com / admin123")
        print("Government Officer:     officer@demo.com / officer123")
        print("Inspector 1:            inspector1@demo.com / inspector123")
        print("Inspector 2:            inspector2@demo.com / inspector123")
        print("Project Representative: representative@demo.com / project123")
        print("-" * 60)
        print("\nNote: All data is SYNTHETIC and for DEMO purposes only.")
        print("No real personal information or government data included.")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n✗ Error during seeding: {str(e)}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
