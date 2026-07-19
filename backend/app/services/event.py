"""Workshop event business operations."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.event import WorkshopEvent
from app.repositories.event import EventRepository
class EventService:
    """Coordinates event lifecycle workflows."""
    def __init__(self, db: Session) -> None: self.repository = EventRepository(db)
    SORT_FIELDS = set(EventRepository.SORT_FIELDS)
    def list(self, search: str | None, event_type: str | None, mode: str | None, featured: bool | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        if sort not in self.SORT_FIELDS: raise HTTPException(422, "Unsupported event sort field")
        if direction not in {"asc", "desc"}: raise HTTPException(422, "Unsupported sort direction")
        return self.repository.list(search, event_type, mode, featured, is_active, sort, direction, page, page_size)
    def get(self, uuid: str): return self._get(uuid)
    def create(self, values: dict): return self.repository.save(WorkshopEvent(**values), {})
    def update(self, uuid: str, values: dict): return self.repository.save(self._get(uuid), values)
    def delete(self, uuid: str): self.repository.save(self._get(uuid), {"is_deleted": True})
    def _get(self, uuid: str) -> WorkshopEvent:
        item = self.repository.get(uuid)
        if item is None: raise HTTPException(status_code=404, detail="Event not found")
        return item
