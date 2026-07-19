"""Student and college contact routes."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.contact import ContactPage, ContactRead, ContactWrite
from app.services.contact import ContactService
router = APIRouter(prefix="/contact", tags=["contact"])
@router.post("", response_model=ContactRead)
def submit_contact(data: ContactWrite, db: Session = Depends(get_db)) -> ContactRead: return ContactService(db).submit(data.model_dump())
@router.get("", response_model=ContactPage, dependencies=[Depends(require("cms:read"))])
def list_contact(contact_type: str | None = None, status: str | None = None, is_read: bool | None = None, archived: bool | None = None, search: str | None = None, sort: str = Query("created_at"), direction: str = Query("desc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> ContactPage:
    items,total=ContactService(db).list(contact_type,status,is_read,archived,search,sort,direction,page,page_size);return ContactPage(items=items,total=total,page=page,page_size=page_size)
@router.get("/{uuid}", response_model=ContactRead, dependencies=[Depends(require("cms:read"))])
def get_contact(uuid: str, db: Session = Depends(get_db)) -> ContactRead: return ContactService(db).get(uuid)
@router.put("/{uuid}", response_model=ContactRead, dependencies=[Depends(require("cms:write"))])
def update_contact(uuid: str, data: ContactWrite, db: Session = Depends(get_db)) -> ContactRead: return ContactService(db).update(uuid, data.model_dump())
@router.post("/{uuid}/read", response_model=ContactRead, dependencies=[Depends(require("cms:write"))])
def mark_contact_read(uuid: str, db: Session = Depends(get_db)) -> ContactRead: return ContactService(db).mark_read(uuid)
@router.post("/{uuid}/status/{status}", response_model=ContactRead, dependencies=[Depends(require("cms:write"))])
def update_contact_status(uuid: str, status: str, db: Session = Depends(get_db)) -> ContactRead:
    """Mark an inquiry read, replied, archived, or new."""
    if status not in {"new", "read", "replied", "archived"}: from fastapi import HTTPException; raise HTTPException(422, "Invalid contact status")
    return ContactService(db).set_status(uuid, status)
@router.delete("/{uuid}", response_model=ContactRead, dependencies=[Depends(require("cms:write"))])
def delete_contact(uuid: str, db: Session = Depends(get_db)) -> ContactRead: return ContactService(db).delete(uuid)
