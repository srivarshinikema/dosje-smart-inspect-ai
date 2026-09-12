"""Report generation service."""

from datetime import datetime
from sqlalchemy.orm import Session
from app.models.inspection import Inspection
from app.models.project import Project
from app.models.user import User
from app.models.evidence import Evidence
from app.models.attendance import Attendance
from app.models.compliance import ComplianceRecord


class ReportService:
    """Report generation logic."""

    @staticmethod
    def generate_inspection_report(
        db: Session, inspection_id: int
    ) -> dict:
        """Generate inspection report data."""
        inspection = db.query(Inspection).filter(
            Inspection.id == inspection_id
        ).first()

        if not inspection:
            return None

        project = db.query(Project).filter(
            Project.id == inspection.project_id
        ).first()
        inspector = db.query(User).filter(
            User.id == inspection.inspector_id
        ).first()

        evidence = db.query(Evidence).filter(
            Evidence.inspection_id == inspection_id
        ).all()
        attendance = db.query(Attendance).filter(
            Attendance.inspection_id == inspection_id
        ).all()
        compliance = db.query(ComplianceRecord).filter(
            ComplianceRecord.inspection_id == inspection_id
        ).all()

        report_data = {
            "report_id": f"RPT-{inspection_id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "generated_at": datetime.utcnow().isoformat(),
            "inspection": {
                "id": inspection.id,
                "status": inspection.status.value,
                "scheduled_date": inspection.scheduled_date.isoformat(),
                "inspection_date": inspection.inspection_date.isoformat() if inspection.inspection_date else None,
                "check_in_time": inspection.check_in_time.isoformat() if inspection.check_in_time else None,
                "check_out_time": inspection.check_out_time.isoformat() if inspection.check_out_time else None,
                "gps_latitude": inspection.gps_latitude,
                "gps_longitude": inspection.gps_longitude,
                "notes": inspection.notes,
                "observations": inspection.observations,
                "risk_score": inspection.risk_score,
            },
            "project": {
                "id": project.id,
                "name": project.name,
                "institute_name": project.institute_name,
                "scheme": project.scheme,
                "location": project.location,
                "latitude": project.latitude,
                "longitude": project.longitude,
                "contact_person": project.contact_person,
                "contact_phone": project.contact_phone,
                "contact_email": project.contact_email,
                "risk_score": project.risk_score,
                "compliance_status": project.compliance_status.value,
            },
            "inspector": {
                "id": inspector.id,
                "name": inspector.full_name or inspector.username,
                "email": inspector.email,
                "role": inspector.role.value,
            },
            "evidence": [
                {
                    "id": e.id,
                    "type": e.file_type,
                    "description": e.description,
                    "gps_latitude": e.gps_latitude,
                    "gps_longitude": e.gps_longitude,
                    "captured_at": e.captured_at.isoformat(),
                }
                for e in evidence
            ],
            "attendance": [
                {
                    "status": a.status.value,
                    "recorded_at": a.recorded_at.isoformat(),
                    "verified_at": a.verified_at.isoformat() if a.verified_at else None,
                }
                for a in attendance
            ],
            "compliance": [
                {
                    "item_name": c.item_name,
                    "status": c.status.value,
                    "remarks": c.remarks,
                    "officer_remarks": c.officer_remarks,
                }
                for c in compliance
            ],
            "summary": {
                "total_evidence_items": len(evidence),
                "attendance_records": len(attendance),
                "compliance_items": len(compliance),
                "duration_minutes": (
                    (inspection.check_out_time - inspection.check_in_time).total_seconds() / 60
                    if inspection.check_in_time and inspection.check_out_time
                    else None
                ),
            },
        }

        return report_data

    @staticmethod
    def generate_pdf_report(report_data: dict) -> bytes:
        """Generate PDF report using ReportLab."""
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            SimpleDocTemplate,
            Table,
            TableStyle,
            Paragraph,
            Spacer,
            PageBreak,
        )
        from reportlab.lib import colors
        import io

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Title
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#003366"),
            spaceAfter=30,
            alignment=1,
        )
        elements.append(
            Paragraph("DoSJE SmartInspect AI - Inspection Report", title_style)
        )
        elements.append(Spacer(1, 0.3 * inch))

        # Report Info
        report_info = [
            ["Report ID:", report_data["report_id"]],
            ["Generated:", report_data["generated_at"]],
            ["Status:", report_data["inspection"]["status"]],
        ]
        info_table = Table(report_info, colWidths=[2 * inch, 4 * inch])
        info_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F4F8")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        elements.append(info_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Project Details
        elements.append(
            Paragraph("Project Information", styles["Heading2"])
        )
        project_data = [
            ["Name:", report_data["project"]["name"]],
            ["Institute:", report_data["project"]["institute_name"]],
            ["Scheme:", report_data["project"]["scheme"]],
            ["Location:", report_data["project"]["location"]],
            ["Risk Score:", str(report_data["project"]["risk_score"])],
            ["Compliance:", report_data["project"]["compliance_status"]],
        ]
        project_table = Table(project_data, colWidths=[2 * inch, 4 * inch])
        project_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F4F8")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ]
            )
        )
        elements.append(project_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Inspector Details
        elements.append(
            Paragraph("Inspector Information", styles["Heading2"])
        )
        inspector_data = [
            ["Name:", report_data["inspector"]["name"]],
            ["Email:", report_data["inspector"]["email"]],
            ["Role:", report_data["inspector"]["role"]],
        ]
        inspector_table = Table(inspector_data, colWidths=[2 * inch, 4 * inch])
        inspector_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F4F8")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ]
            )
        )
        elements.append(inspector_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Summary
        elements.append(
            Paragraph("Inspection Summary", styles["Heading2"])
        )
        summary_data = [
            ["Evidence Items:", str(report_data["summary"]["total_evidence_items"])],
            ["Attendance Records:", str(report_data["summary"]["attendance_records"])],
            ["Compliance Items:", str(report_data["summary"]["compliance_items"])],
        ]
        summary_table = Table(summary_data, colWidths=[2 * inch, 4 * inch])
        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F4F8")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ]
            )
        )
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Footer
        footer_style = ParagraphStyle(
            "Footer",
            parent=styles["Normal"],
            fontSize=8,
            textColor=colors.grey,
            alignment=1,
        )
        elements.append(
            Paragraph(
                f"This is an automated inspection report generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}. "
                "For official use only.",
                footer_style,
            )
        )

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
