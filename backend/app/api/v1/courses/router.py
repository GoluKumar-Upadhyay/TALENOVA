"""Full LMS Courses API router."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.course import (
    ApplicationPage, ApplicationRead, ApplicationStatusUpdate, ApplicationWrite,
    BatchRead, BatchWrite,
    CoursePage, CourseRead, CourseCreate, CourseUpdate,
    ModuleRead, ModuleReorder, ModuleWrite,
    SubmoduleRead, SubmoduleWrite,
)
from app.services.course import CourseService

router = APIRouter(prefix="/courses", tags=["courses"])

AUTH = [Depends(require("cms:write"))]


# ── Courses ───────────────────────────────────────────────────────────────────

@router.get("", response_model=CoursePage)
def list_courses(
    search: str | None = None,
    category_id: int | None = None,
    mentor_id: int | None = None,
    published: bool | None = None,
    coming_soon: bool | None = None,
    is_active: bool | None = None,
    sort: str = Query("display_order"),
    direction: str = Query("asc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(24, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = CourseService(db).list(
        search, category_id, mentor_id, published, coming_soon, is_active,
        sort, direction, page, page_size,
    )
    return CoursePage(items=items, total=total, page=page, page_size=page_size)


@router.post("", response_model=CourseRead, dependencies=AUTH)
def create_course(data: CourseCreate, db: Session = Depends(get_db)):
    return CourseService(db).create(data.model_dump())


@router.get("/slug/{slug}", response_model=CourseRead)
def get_course_by_slug(slug: str, db: Session = Depends(get_db)):
    return CourseService(db).get_by_slug(slug)


@router.get("/{uuid}", response_model=CourseRead)
def get_course(uuid: str, db: Session = Depends(get_db)):
    return CourseService(db).get(uuid)


@router.put("/{uuid}", response_model=CourseRead, dependencies=AUTH)
def update_course(uuid: str, data: CourseUpdate, db: Session = Depends(get_db)):
    return CourseService(db).update(uuid, data.model_dump(exclude_unset=True))


@router.delete("/{uuid}", dependencies=AUTH)
def delete_course(uuid: str, db: Session = Depends(get_db)):
    CourseService(db).delete(uuid)
    return {"deleted": True}


# ── Modules ───────────────────────────────────────────────────────────────────

@router.get("/{uuid}/modules", response_model=list[ModuleRead])
def list_modules(uuid: str, db: Session = Depends(get_db)):
    return CourseService(db).list_modules(uuid)


@router.post("/{uuid}/modules", response_model=ModuleRead, dependencies=AUTH)
def create_module(uuid: str, data: ModuleWrite, db: Session = Depends(get_db)):
    return CourseService(db).create_module(uuid, data.model_dump())


@router.put("/{uuid}/modules/reorder", response_model=list[ModuleRead], dependencies=AUTH)
def reorder_modules(uuid: str, body: ModuleReorder, db: Session = Depends(get_db)):
    return CourseService(db).reorder_modules(uuid, body.ordered_uuids)


@router.get("/{uuid}/modules/{mod_uuid}", response_model=ModuleRead)
def get_module(uuid: str, mod_uuid: str, db: Session = Depends(get_db)):
    return CourseService(db).get_module(mod_uuid)


@router.put("/{uuid}/modules/{mod_uuid}", response_model=ModuleRead, dependencies=AUTH)
def update_module(uuid: str, mod_uuid: str, data: ModuleWrite, db: Session = Depends(get_db)):
    return CourseService(db).update_module(mod_uuid, data.model_dump(exclude_unset=True))


@router.delete("/{uuid}/modules/{mod_uuid}", dependencies=AUTH)
def delete_module(uuid: str, mod_uuid: str, db: Session = Depends(get_db)):
    CourseService(db).delete_module(mod_uuid)
    return {"deleted": True}


# ── Submodules ────────────────────────────────────────────────────────────────

@router.post("/{uuid}/modules/{mod_uuid}/submodules", response_model=SubmoduleRead, dependencies=AUTH)
def create_submodule(uuid: str, mod_uuid: str, data: SubmoduleWrite, db: Session = Depends(get_db)):
    return CourseService(db).create_submodule(mod_uuid, data.model_dump())


@router.put("/{uuid}/modules/{mod_uuid}/submodules/reorder", response_model=list[SubmoduleRead], dependencies=AUTH)
def reorder_submodules(uuid: str, mod_uuid: str, body: ModuleReorder, db: Session = Depends(get_db)):
    return CourseService(db).reorder_submodules(mod_uuid, body.ordered_uuids)


@router.put("/{uuid}/modules/{mod_uuid}/submodules/{sub_uuid}", response_model=SubmoduleRead, dependencies=AUTH)
def update_submodule(uuid: str, mod_uuid: str, sub_uuid: str, data: SubmoduleWrite, db: Session = Depends(get_db)):
    return CourseService(db).update_submodule(sub_uuid, data.model_dump(exclude_unset=True))


@router.delete("/{uuid}/modules/{mod_uuid}/submodules/{sub_uuid}", dependencies=AUTH)
def delete_submodule(uuid: str, mod_uuid: str, sub_uuid: str, db: Session = Depends(get_db)):
    CourseService(db).delete_submodule(sub_uuid)
    return {"deleted": True}


# ── Batches ───────────────────────────────────────────────────────────────────

@router.get("/{uuid}/batches", response_model=list[BatchRead])
def list_batches(uuid: str, db: Session = Depends(get_db)):
    return CourseService(db).list_batches(uuid)


@router.post("/{uuid}/batches", response_model=BatchRead, dependencies=AUTH)
def create_batch(uuid: str, data: BatchWrite, db: Session = Depends(get_db)):
    return CourseService(db).create_batch(uuid, data.model_dump())


@router.put("/{uuid}/batches/{batch_uuid}", response_model=BatchRead, dependencies=AUTH)
def update_batch(uuid: str, batch_uuid: str, data: BatchWrite, db: Session = Depends(get_db)):
    return CourseService(db).update_batch(batch_uuid, data.model_dump(exclude_unset=True))


@router.delete("/{uuid}/batches/{batch_uuid}", dependencies=AUTH)
def delete_batch(uuid: str, batch_uuid: str, db: Session = Depends(get_db)):
    CourseService(db).delete_batch(batch_uuid)
    return {"deleted": True}


# ── Applications ──────────────────────────────────────────────────────────────

@router.get("/{uuid}/applications", response_model=ApplicationPage, dependencies=AUTH)
def list_applications(
    uuid: str,
    search: str | None = None,
    status: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    items, total = CourseService(db).list_applications(uuid, search, status, page, page_size)
    return ApplicationPage(items=items, total=total, page=page, page_size=page_size)


@router.post("/{uuid}/applications", response_model=ApplicationRead)
def submit_application(uuid: str, data: ApplicationWrite, db: Session = Depends(get_db)):
    """Public endpoint — no auth required."""
    return CourseService(db).submit_application(uuid, data.model_dump())


@router.put("/{uuid}/applications/{app_uuid}", response_model=ApplicationRead, dependencies=AUTH)
def update_application(uuid: str, app_uuid: str, data: ApplicationStatusUpdate, db: Session = Depends(get_db)):
    return CourseService(db).update_application(app_uuid, data.model_dump(exclude_unset=True))
