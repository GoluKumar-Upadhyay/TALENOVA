"""Website settings persistence."""

from __future__ import annotations
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.settings import WebsiteSettings
class SettingsRepository:
    """Accesses the settings singleton."""
    SORT_FIELDS = {"site_name": WebsiteSettings.site_name, "updated_at": WebsiteSettings.updated_at, "default_language": WebsiteSettings.default_language}
    def __init__(self, db: Session) -> None: self.db = db
    def get(self) -> WebsiteSettings | None: return self.db.scalar(select(WebsiteSettings).limit(1))
    def list(self, maintenance_mode: bool | None, sort: str, direction: str, page: int, page_size: int):
        filters = []
        if maintenance_mode is not None: filters.append(WebsiteSettings.maintenance_mode == maintenance_mode)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(WebsiteSettings).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(WebsiteSettings).where(*filters)) or 0
    def get_by_uuid(self, uuid: str): return self.db.scalar(select(WebsiteSettings).where(WebsiteSettings.uuid == uuid))
    def save(self, item: WebsiteSettings, values: dict) -> WebsiteSettings:
        for field, value in values.items(): setattr(item, field, value)
        self.db.add(item); self.db.commit(); self.db.refresh(item); return item
    def delete(self, item: WebsiteSettings) -> None:
        self.db.delete(item); self.db.commit()
