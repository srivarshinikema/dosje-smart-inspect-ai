"""Evidence model."""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from datetime import datetime
from app.models import Base


class Evidence(Base):
    """Evidence model."""

    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    inspector_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # image, video, document
    gps_latitude = Column(Float, nullable=True)
    gps_longitude = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    captured_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Evidence {self.id}>"
