"""Navigation REST API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.services.navigation import NavigationService
from app.schemas.navigation import NavigationPage, NavigationRead, NavigationWrite
router = APIRouter(prefix="/navigation", tags=["navigation"])
@router.get("", response_model=NavigationPage)
def list_navigation(location: str | None = None, search: str | None = None, is_active: bool | None = None, sort: str = Query("display_order"), direction: str = Query("asc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> NavigationPage:
    items,total=NavigationService(db).list(location,search,is_active,sort,direction,page,page_size);return NavigationPage(items=items,total=total,page=page,page_size=page_size)
@router.get("/{uuid}", response_model=NavigationRead)
def get_navigation(uuid: str, db: Session = Depends(get_db)) -> NavigationRead:
    return NavigationService(db).get(uuid)
@router.post("", response_model=NavigationRead, dependencies=[Depends(require("cms:write"))])
def create_navigation(data: NavigationWrite, db: Session = Depends(get_db)) -> NavigationRead:
    return NavigationService(db).create(data.model_dump())
@router.put("/{uuid}", response_model=NavigationRead, dependencies=[Depends(require("cms:write"))])
def update_navigation(uuid: str, data: NavigationWrite, db: Session = Depends(get_db)) -> NavigationRead:
    return NavigationService(db).update(uuid, data.model_dump())
@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_navigation(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    NavigationService(db).delete(uuid); return {"deleted": True}
