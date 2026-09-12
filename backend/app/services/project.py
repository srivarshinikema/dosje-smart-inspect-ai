"""Project service."""

from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    """Project business logic."""

    @staticmethod
    def create_project(db: Session, project: ProjectCreate) -> Project:
        """Create a new project."""
        db_project = Project(**project.dict())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def get_project(db: Session, project_id: int) -> Project:
        """Get project by ID."""
        return db.query(Project).filter(Project.id == project_id).first()

    @staticmethod
    def list_projects(db: Session, skip: int = 0, limit: int = 100) -> list:
        """List all projects."""
        return db.query(Project).offset(skip).limit(limit).all()

    @staticmethod
    def update_project(db: Session, project_id: int, project: ProjectUpdate) -> Project:
        """Update a project."""
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project:
            update_data = project.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_project, field, value)
            db.commit()
            db.refresh(db_project)
        return db_project

    @staticmethod
    def delete_project(db: Session, project_id: int) -> bool:
        """Delete a project."""
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project:
            db.delete(db_project)
            db.commit()
            return True
        return False

    @staticmethod
    def search_projects(db: Session, search_term: str) -> list:
        """Search projects by name or institute."""
        return db.query(Project).filter(
            (Project.name.ilike(f"%{search_term}%")) |
            (Project.institute_name.ilike(f"%{search_term}%"))
        ).all()

    @staticmethod
    def get_high_risk_projects(db: Session, threshold: float = 70.0) -> list:
        """Get projects with risk score above threshold."""
        return db.query(Project).filter(Project.risk_score >= threshold).all()
