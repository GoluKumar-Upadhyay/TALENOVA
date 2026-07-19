"""Footer REST API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.footer import FooterPage, FooterRead, FooterWrite
from app.services.footer import FooterService
router = APIRouter(prefix="/footer", tags=["footer"])
@router.get("", response_model=FooterRead)
def get_footer(db: Session = Depends(get_db)) -> FooterRead: return FooterService(db).get()
@router.get("/all", response_model=FooterPage, dependencies=[Depends(require("cms:read"))])
def list_footer(is_active: bool | None = None, sort: str = Query("updated_at"), direction: str = Query("desc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> FooterPage:
    items,total=FooterService(db).list(is_active,sort,direction,page,page_size);return FooterPage(items=items,total=total,page=page,page_size=page_size)
@router.post("", response_model=FooterRead, dependencies=[Depends(require("cms:write"))])
def create_footer(data: FooterWrite, db: Session = Depends(get_db)) -> FooterRead: return FooterService(db).create(data.model_dump())
@router.put("", response_model=FooterRead, dependencies=[Depends(require("cms:write"))])
def save_footer(data: FooterWrite, db: Session = Depends(get_db)) -> FooterRead: return FooterService(db).save(data.model_dump())
@router.get("/{uuid}", response_model=FooterRead, dependencies=[Depends(require("cms:read"))])
def get_footer_by_uuid(uuid: str, db: Session = Depends(get_db)) -> FooterRead: return FooterService(db).get_by_uuid(uuid)
@router.put("/{uuid}", response_model=FooterRead, dependencies=[Depends(require("cms:write"))])
def update_footer(uuid: str, data: FooterWrite, db: Session = Depends(get_db)) -> FooterRead: return FooterService(db).update(uuid, data.model_dump())
@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_footer(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]: FooterService(db).delete(uuid); return {"deleted": True}
