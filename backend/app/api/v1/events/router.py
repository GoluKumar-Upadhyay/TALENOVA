"""Workshop event REST API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.event import EventPage, EventRead, EventWrite
from app.services.event import EventService
router = APIRouter(prefix="/events", tags=["events"])
@router.get("", response_model=EventPage)
def list_events(search: str | None = None, event_type: str | None = None, mode: str | None = None, featured: bool | None = None, is_active: bool | None = None, sort: str = Query("display_order"), direction: str = Query("asc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> EventPage:
    items, total = EventService(db).list(search, event_type, mode, featured, is_active, sort, direction, page, page_size)
    return EventPage(items=items, total=total, page=page, page_size=page_size)
@router.get("/{uuid}", response_model=EventRead)
def get_event(uuid: str, db: Session = Depends(get_db)) -> EventRead: return EventService(db).get(uuid)
@router.post("", response_model=EventRead, dependencies=[Depends(require("cms:write"))])
def create_event(data: EventWrite, db: Session = Depends(get_db)) -> EventRead: return EventService(db).create(data.model_dump())
@router.put("/{uuid}", response_model=EventRead, dependencies=[Depends(require("cms:write"))])
def update_event(uuid: str, data: EventWrite, db: Session = Depends(get_db)) -> EventRead: return EventService(db).update(uuid, data.model_dump())
@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_event(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]: EventService(db).delete(uuid); return {"deleted": True}
