"""Project REST API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.project import ProjectPage, ProjectRead, ProjectWrite
from app.services.project import ProjectService
router = APIRouter(prefix="/projects", tags=["projects"])
@router.get("", response_model=ProjectPage)
def list_projects(search: str | None = None, status: str | None = None, featured: bool | None = None, is_active: bool | None = None, sort: str = Query("display_order"), direction: str = Query("asc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> ProjectPage:
    """List projects by display order."""
    items, total = ProjectService(db).list(search, status, featured, is_active, sort, direction, page, page_size)
    return ProjectPage(items=items, total=total, page=page, page_size=page_size)
@router.get("/{uuid}", response_model=ProjectRead)
def get_project(uuid: str, db: Session = Depends(get_db)) -> ProjectRead:
    """Get project by id."""
    return ProjectService(db).get(uuid)
@router.post("", response_model=ProjectRead, dependencies=[Depends(require("cms:write"))])
def create_project(data: ProjectWrite, db: Session = Depends(get_db)) -> ProjectRead:
    """Create project."""
    return ProjectService(db).create(data.model_dump())
@router.put("/{uuid}", response_model=ProjectRead, dependencies=[Depends(require("cms:write"))])
def update_project(uuid: str, data: ProjectWrite, db: Session = Depends(get_db)) -> ProjectRead:
    """Update project."""
    return ProjectService(db).update(uuid, data.model_dump())
@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_project(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    """Soft-delete project."""
    ProjectService(db).delete(uuid)
    return {"deleted": True}
