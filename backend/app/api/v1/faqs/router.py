"""FAQ REST API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.faq import FAQPage, FAQRead, FAQWrite
from app.services.faq import FAQService
router = APIRouter(prefix="/faqs", tags=["faqs"])
@router.get("", response_model=FAQPage)
def list_faqs(search: str | None = None, page_key: str | None = None, category: str | None = None, featured: bool | None = None, is_active: bool | None = None, sort: str = Query("display_order"), direction: str = Query("asc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> FAQPage:
    items, total = FAQService(db).list(search, page_key, category, featured, is_active, sort, direction, page, page_size)
    return FAQPage(items=items, total=total, page=page, page_size=page_size)
@router.get("/{uuid}", response_model=FAQRead)
def get_faq(uuid: str, db: Session = Depends(get_db)) -> FAQRead: return FAQService(db).get(uuid)
@router.post("", response_model=FAQRead, dependencies=[Depends(require("cms:write"))])
def create_faq(data: FAQWrite, db: Session = Depends(get_db)) -> FAQRead: return FAQService(db).create(data.model_dump())
@router.put("/{uuid}", response_model=FAQRead, dependencies=[Depends(require("cms:write"))])
def update_faq(uuid: str, data: FAQWrite, db: Session = Depends(get_db)) -> FAQRead: return FAQService(db).update(uuid, data.model_dump())
@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_faq(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]: FAQService(db).delete(uuid); return {"deleted": True}
