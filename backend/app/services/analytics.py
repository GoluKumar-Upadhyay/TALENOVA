"""Dashboard analytics business service."""
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.analytics import AnalyticsEvent
from app.repositories.analytics import AnalyticsRepository
class AnalyticsService:
    """Builds dashboard data from indexed aggregate event queries."""
    SORT_FIELDS = set(AnalyticsRepository.SORT_FIELDS)
    def __init__(self, db: Session) -> None: self.repository = AnalyticsRepository(db)
    def dashboard(self, start=None, end=None) -> dict:
        counts = dict(self.repository.event_counts(start, end))
        summary = {key: counts.get(key, 0) for key in ("courses", "students", "teachers", "contacts", "events", "internships", "testimonials", "success_stories", "gallery_images", "videos")}
        return {"summary": {f"total_{key}": value for key, value in summary.items()}, "monthly_contacts": [], "monthly_events": [], "monthly_internships": [], "recent_activities": [{"event_type": item.event_type, "occurred_at": item.occurred_at.isoformat()} for item in self.repository.recent()]}
    def list(self, search: str | None, event_type: str | None, start=None, end=None, sort: str = "occurred_at", direction: str = "desc", page: int = 1, page_size: int = 24):
        if sort not in self.SORT_FIELDS: raise HTTPException(422, "Unsupported analytics sort field")
        if direction not in {"asc", "desc"}: raise HTTPException(422, "Unsupported sort direction")
        return self.repository.list(search, event_type, start, end, sort, direction, page, page_size)
    def get(self, uuid: str):
        item = self.repository.get(uuid)
        if item is None: raise HTTPException(404, "Analytics event not found")
        return item
    def create(self, values: dict):
        values["occurred_at"] = values.get("occurred_at") or datetime.utcnow()
        return self.repository.save(AnalyticsEvent(**values), {})
    def update(self, uuid: str, values: dict):
        values["occurred_at"] = values.get("occurred_at") or self.get(uuid).occurred_at
        return self.repository.save(self.get(uuid), values)
    def delete(self, uuid: str) -> None:
        self.repository.delete(self.get(uuid))
