"""Internship REST API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.internship import InternshipPage, InternshipRead, InternshipWrite
from app.services.internship import InternshipService
router = APIRouter(prefix="/internships", tags=["internships"])
@router.get("", response_model=InternshipPage)
def list_internships(search: str | None = None, internship_type: str | None = None, featured: bool | None = None, coming_soon: bool | None = None, is_active: bool | None = None, sort: str = Query("display_order"), direction: str = Query("asc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> InternshipPage:
    items, total = InternshipService(db).list(search, internship_type, featured, coming_soon, is_active, sort, direction, page, page_size)
    return InternshipPage(items=items, total=total, page=page, page_size=page_size)
@router.get("/{uuid}", response_model=InternshipRead)
def get_internship(uuid: str, db: Session = Depends(get_db)) -> InternshipRead: return InternshipService(db).get(uuid)
@router.post("", response_model=InternshipRead, dependencies=[Depends(require("cms:write"))])
def create_internship(data: InternshipWrite, db: Session = Depends(get_db)) -> InternshipRead: return InternshipService(db).create(data.model_dump())
@router.put("/{uuid}", response_model=InternshipRead, dependencies=[Depends(require("cms:write"))])
def update_internship(uuid: str, data: InternshipWrite, db: Session = Depends(get_db)) -> InternshipRead: return InternshipService(db).update(uuid, data.model_dump())
@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_internship(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]: InternshipService(db).delete(uuid); return {"deleted": True}
