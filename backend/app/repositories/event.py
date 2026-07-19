"""Workshop event persistence."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.event import WorkshopEvent
class EventRepository:
    """Database queries for workshop events."""
    def __init__(self, db: Session) -> None: self.db = db
    SORT_FIELDS = {"title": WorkshopEvent.title, "display_order": WorkshopEvent.display_order, "created_at": WorkshopEvent.created_at, "start_date": WorkshopEvent.start_date}
    def list(self, search: str | None, event_type: str | None, mode: str | None, featured: bool | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[WorkshopEvent], int]:
        filters = [WorkshopEvent.is_deleted.is_(False)]
        if search: filters.append(WorkshopEvent.title.ilike(f"%{search}%"))
        if event_type: filters.append(WorkshopEvent.event_type == event_type)
        if mode: filters.append(WorkshopEvent.mode == mode)
        if featured is not None: filters.append(WorkshopEvent.is_featured == featured)
        if is_active is not None: filters.append(WorkshopEvent.is_active == is_active)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(WorkshopEvent).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(WorkshopEvent).where(*filters)) or 0
    def get(self, uuid: str) -> WorkshopEvent | None: return self.db.scalar(select(WorkshopEvent).where(WorkshopEvent.uuid == uuid, WorkshopEvent.is_deleted.is_(False)))
    def save(self, item: WorkshopEvent, values: dict) -> WorkshopEvent:
        for field, value in values.items(): setattr(item, field, value)
        self.db.add(item); self.db.commit(); self.db.refresh(item); return item
