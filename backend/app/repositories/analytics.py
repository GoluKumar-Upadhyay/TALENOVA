"""Optimized dashboard aggregate queries."""

from __future__ import annotations
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.analytics import AnalyticsEvent
class AnalyticsRepository:
    """Reads aggregate counts without loading content rows."""
    SORT_FIELDS = {"event_type": AnalyticsEvent.event_type, "occurred_at": AnalyticsEvent.occurred_at}
    def __init__(self, db: Session) -> None: self.db = db
    def event_counts(self, start=None, end=None) -> list[tuple[str, int]]:
        filters = []
        if start: filters.append(AnalyticsEvent.occurred_at >= start)
        if end: filters.append(AnalyticsEvent.occurred_at <= end)
        query = select(AnalyticsEvent.event_type, func.count()).where(*filters).group_by(AnalyticsEvent.event_type)
        return list(self.db.execute(query))
    def recent(self, limit: int = 10) -> list[AnalyticsEvent]:
        return list(self.db.scalars(select(AnalyticsEvent).order_by(AnalyticsEvent.occurred_at.desc()).limit(limit)))
    def list(self, search: str | None, event_type: str | None, start=None, end=None, sort: str = "occurred_at", direction: str = "desc", page: int = 1, page_size: int = 24):
        filters = []
        if search: filters.append(AnalyticsEvent.event_type.ilike(f"%{search}%"))
        if event_type: filters.append(AnalyticsEvent.event_type == event_type)
        if start: filters.append(AnalyticsEvent.occurred_at >= start)
        if end: filters.append(AnalyticsEvent.occurred_at <= end)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(AnalyticsEvent).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(AnalyticsEvent).where(*filters)) or 0
    def get(self, uuid: str) -> AnalyticsEvent | None:
        return self.db.scalar(select(AnalyticsEvent).where(AnalyticsEvent.uuid == uuid))
    def save(self, item: AnalyticsEvent, values: dict) -> AnalyticsEvent:
        for key, value in values.items():
            setattr(item, key, value)
        self.db.add(item); self.db.commit(); self.db.refresh(item); return item
    def delete(self, item: AnalyticsEvent) -> None:
        self.db.delete(item); self.db.commit()
