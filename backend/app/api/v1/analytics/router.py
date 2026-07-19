"""Admin dashboard analytics API."""
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.analytics import AnalyticsEventPage, AnalyticsEventRead, AnalyticsEventWrite, AnalyticsResponse
from app.services.analytics import AnalyticsService
router = APIRouter(prefix="/analytics", tags=["analytics"])
@router.get("", response_model=AnalyticsEventPage, dependencies=[Depends(require("users:manage"))])
def list_events(search: str | None = None, event_type: str | None = None, start: date | None = None, end: date | None = None, sort: str = Query("occurred_at"), direction: str = Query("desc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> AnalyticsEventPage:
    items,total=AnalyticsService(db).list(search,event_type,start,end,sort,direction,page,page_size);return AnalyticsEventPage(items=items,total=total,page=page,page_size=page_size)
@router.post("", response_model=AnalyticsEventRead, dependencies=[Depends(require("users:manage"))])
def create_event(data: AnalyticsEventWrite, db: Session = Depends(get_db)) -> AnalyticsEventRead:
    return AnalyticsService(db).create(data.model_dump())
@router.get("/dashboard", response_model=AnalyticsResponse, dependencies=[Depends(require("users:manage"))])
def dashboard(start: date | None = None, end: date | None = None, db: Session = Depends(get_db)) -> AnalyticsResponse:
    """Return admin-only summary cards and recent activity."""
    return AnalyticsService(db).dashboard(start, end)
@router.get("/{uuid}", response_model=AnalyticsEventRead, dependencies=[Depends(require("users:manage"))])
def get_event(uuid: str, db: Session = Depends(get_db)) -> AnalyticsEventRead:
    return AnalyticsService(db).get(uuid)
@router.put("/{uuid}", response_model=AnalyticsEventRead, dependencies=[Depends(require("users:manage"))])
def update_event(uuid: str, data: AnalyticsEventWrite, db: Session = Depends(get_db)) -> AnalyticsEventRead:
    return AnalyticsService(db).update(uuid, data.model_dump())
@router.delete("/{uuid}", dependencies=[Depends(require("users:manage"))])
def delete_event(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    AnalyticsService(db).delete(uuid); return {"deleted": True}
