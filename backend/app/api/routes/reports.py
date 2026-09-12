"""Report routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User, UserRole
from app.services.report import ReportService
import tempfile
import os

router = APIRouter()


@router.get("/{inspection_id}/data")
def get_inspection_report_data(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get inspection report data as JSON."""
    report_data = ReportService.generate_inspection_report(db, inspection_id)
    if not report_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection not found",
        )
    return report_data


@router.get("/{inspection_id}/pdf")
def get_inspection_report_pdf(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get inspection report as PDF."""
    if current_user.role not in [UserRole.ADMIN, UserRole.GOVERNMENT_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to download reports",
        )

    report_data = ReportService.generate_inspection_report(db, inspection_id)
    if not report_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection not found",
        )

    # Generate PDF
    pdf_content = ReportService.generate_pdf_report(report_data)

    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_content)
        tmp_path = tmp.name

    return FileResponse(
        tmp_path,
        media_type="application/pdf",
        filename=f"inspection_report_{inspection_id}.pdf",
    )
