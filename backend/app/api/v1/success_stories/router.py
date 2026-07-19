"""Success story REST API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.success_story import SuccessStoryPage, SuccessStoryRead, SuccessStoryWrite
from app.services.success_story import SuccessStoryService
router = APIRouter(prefix="/success-stories", tags=["success stories"])
@router.get("", response_model=SuccessStoryPage)
def list_stories(search: str | None = None, featured: bool | None = None, is_active: bool | None = None, course: str | None = None, sort: str = Query("display_order"), direction: str = Query("asc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> SuccessStoryPage:
    items, total = SuccessStoryService(db).list(search, featured, is_active, course, sort, direction, page, page_size)
    return SuccessStoryPage(items=items, total=total, page=page, page_size=page_size)
@router.get("/{uuid}", response_model=SuccessStoryRead)
def get_story(uuid: str, db: Session = Depends(get_db)) -> SuccessStoryRead: return SuccessStoryService(db).get(uuid)
@router.post("", response_model=SuccessStoryRead, dependencies=[Depends(require("cms:write"))])
def create_story(data: SuccessStoryWrite, db: Session = Depends(get_db)) -> SuccessStoryRead: return SuccessStoryService(db).create(data.model_dump())
@router.put("/{uuid}", response_model=SuccessStoryRead, dependencies=[Depends(require("cms:write"))])
def update_story(uuid: str, data: SuccessStoryWrite, db: Session = Depends(get_db)) -> SuccessStoryRead: return SuccessStoryService(db).update(uuid, data.model_dump())
@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_story(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]: SuccessStoryService(db).delete(uuid); return {"deleted": True}
