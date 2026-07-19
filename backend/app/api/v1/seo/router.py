"""SEO REST API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.seo import SEOPage, SEORead, SEOWrite
from app.services.seo import SEOService
router = APIRouter(prefix="/seo", tags=["seo"])
@router.get("", response_model=SEOPage)
def list_seo(search: str | None = None, is_active: bool | None = True, sort: str = Query("page_key"), direction: str = Query("asc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> SEOPage:
    items,total=SEOService(db).list(search,is_active,sort,direction,page,page_size);return SEOPage(items=items,total=total,page=page,page_size=page_size)
@router.post("", response_model=SEORead, dependencies=[Depends(require("cms:write"))])
def create_seo(data: SEOWrite, db: Session = Depends(get_db)) -> SEORead: return SEOService(db).create(data.model_dump())
@router.put("", response_model=SEORead, dependencies=[Depends(require("cms:write"))])
def save_seo(data: SEOWrite, db: Session = Depends(get_db)) -> SEORead: return SEOService(db).save(data.model_dump())
@router.get("/page/{page_key}", response_model=SEORead)
def get_seo_page(page_key: str, db: Session = Depends(get_db)) -> SEORead: return SEOService(db).get(page_key)
@router.get("/{uuid}", response_model=SEORead)
def get_seo(uuid: str, db: Session = Depends(get_db)) -> SEORead: return SEOService(db).get_by_uuid(uuid)
@router.put("/{uuid}", response_model=SEORead, dependencies=[Depends(require("cms:write"))])
def update_seo(uuid: str, data: SEOWrite, db: Session = Depends(get_db)) -> SEORead: return SEOService(db).update(uuid, data.model_dump())
@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_seo(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]: SEOService(db).delete(uuid); return {"deleted": True}
