"""SEO persistence."""

from __future__ import annotations
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.seo import SEORecord
class SEORepository:
    """Accesses page SEO records."""
    SORT_FIELDS = {"page_key": SEORecord.page_key, "meta_title": SEORecord.meta_title, "updated_at": SEORecord.updated_at}
    def __init__(self, db: Session) -> None: self.db = db
    def list(self, search: str | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        filters = []
        if search: filters.append(SEORecord.page_key.ilike(f"%{search}%") | SEORecord.meta_title.ilike(f"%{search}%"))
        if is_active is not None: filters.append(SEORecord.is_active == is_active)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(SEORecord).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(SEORecord).where(*filters)) or 0
    def get(self, page_key: str): return self.db.scalar(select(SEORecord).where(SEORecord.page_key == page_key))
    def get_by_uuid(self, uuid: str): return self.db.scalar(select(SEORecord).where(SEORecord.uuid == uuid))
    def save(self, item: SEORecord, values: dict):
        for field, value in values.items(): setattr(item, field, value)
        self.db.add(item); self.db.commit(); self.db.refresh(item); return item
    def delete(self, item: SEORecord) -> None:
        self.db.delete(item); self.db.commit()
