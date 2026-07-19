"""Teacher REST API routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.teacher import TeacherPage, TeacherRead, TeacherWrite
from app.services.teacher import TeacherService

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get("", response_model=TeacherPage)
def list_teachers(
    search: str | None = None,
    designation: str | None = None,
    is_active: bool | None = None,
    sort: str = Query(default="display_order"),
    direction: str = Query(default="asc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=24, ge=1, le=100),
    db: Session = Depends(get_db),
) -> TeacherPage:
    """List teachers in configured display order."""

    items, total = TeacherService(db).list(search, designation, is_active, sort, direction, page, page_size)
    return TeacherPage(items=items, total=total, page=page, page_size=page_size)


@router.get("/{uuid}", response_model=TeacherRead)
def get_teacher(uuid: str, db: Session = Depends(get_db)) -> TeacherRead:
    """Get a teacher profile."""

    return TeacherService(db).get(uuid)


@router.post("", response_model=TeacherRead, dependencies=[Depends(require("cms:write"))])
def create_teacher(data: TeacherWrite, db: Session = Depends(get_db)) -> TeacherRead:
    """Create a teacher profile."""

    return TeacherService(db).create(data.model_dump())


@router.put("/{uuid}", response_model=TeacherRead, dependencies=[Depends(require("cms:write"))])
def update_teacher(uuid: str, data: TeacherWrite, db: Session = Depends(get_db)) -> TeacherRead:
    """Update a teacher profile."""

    return TeacherService(db).update(uuid, data.model_dump())


@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_teacher(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    """Soft-delete a teacher profile."""

    TeacherService(db).delete(uuid)
    return {"deleted": True}
