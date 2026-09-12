"""Project routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User, UserRole
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project import ProjectService

router = APIRouter()


@router.get("/", response_model=list[ProjectResponse])
def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all projects."""
    return ProjectService.list_projects(db, skip=skip, limit=limit)


@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new project. Admin and Government Officer only."""
    if current_user.role not in [UserRole.ADMIN, UserRole.GOVERNMENT_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create projects"
        )
    return ProjectService.create_project(db, project)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get project by ID."""
    db_project = ProjectService.get_project(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db_project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a project. Admin and Government Officer only."""
    if current_user.role not in [UserRole.ADMIN, UserRole.GOVERNMENT_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update projects"
        )
    
    db_project = ProjectService.get_project(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return ProjectService.update_project(db, project_id, project)


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a project. Admin only."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete projects"
        )
    
    success = ProjectService.delete_project(db, project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return {"message": "Project deleted successfully"}


@router.get("/search/{search_term}", response_model=list[ProjectResponse])
def search_projects(
    search_term: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search projects by name or institute."""
    return ProjectService.search_projects(db, search_term)


@router.get("/high-risk/list", response_model=list[ProjectResponse])
def get_high_risk_projects(
    threshold: float = 70.0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get high-risk projects."""
    if current_user.role not in [UserRole.ADMIN, UserRole.GOVERNMENT_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view high-risk projects"
        )
    return ProjectService.get_high_risk_projects(db, threshold=threshold)
