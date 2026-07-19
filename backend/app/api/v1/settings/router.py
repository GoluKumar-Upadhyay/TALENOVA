"""Website settings REST API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.settings import SettingsPage, SettingsRead, SettingsWrite
from app.services.settings import SettingsService
router = APIRouter(prefix="/settings", tags=["settings"])
@router.get("", response_model=SettingsRead)
def get_settings(db: Session = Depends(get_db)) -> SettingsRead: return SettingsService(db).get()
@router.get("/all", response_model=SettingsPage, dependencies=[Depends(require("cms:read"))])
def list_settings(maintenance_mode: bool | None = None, sort: str = Query("updated_at"), direction: str = Query("desc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> SettingsPage:
    items,total=SettingsService(db).list(maintenance_mode,sort,direction,page,page_size);return SettingsPage(items=items,total=total,page=page,page_size=page_size)
@router.post("", response_model=SettingsRead, dependencies=[Depends(require("cms:write"))])
def create_settings(data: SettingsWrite, db: Session = Depends(get_db)) -> SettingsRead: return SettingsService(db).create(data.model_dump())
@router.put("", response_model=SettingsRead, dependencies=[Depends(require("cms:write"))])
def save_settings(data: SettingsWrite, db: Session = Depends(get_db)) -> SettingsRead: return SettingsService(db).save(data.model_dump())
@router.get("/{uuid}", response_model=SettingsRead, dependencies=[Depends(require("cms:read"))])
def get_settings_by_uuid(uuid: str, db: Session = Depends(get_db)) -> SettingsRead: return SettingsService(db).get_by_uuid(uuid)
@router.put("/{uuid}", response_model=SettingsRead, dependencies=[Depends(require("cms:write"))])
def update_settings(uuid: str, data: SettingsWrite, db: Session = Depends(get_db)) -> SettingsRead: return SettingsService(db).update(uuid, data.model_dump())
@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_settings(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]: SettingsService(db).delete(uuid); return {"deleted": True}
