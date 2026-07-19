"""Footer persistence."""

from __future__ import annotations
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.footer import FooterConfiguration
class FooterRepository:
    """Accesses footer singleton."""
    SORT_FIELDS = {"display_order": FooterConfiguration.display_order, "updated_at": FooterConfiguration.updated_at}
    def __init__(self, db: Session) -> None: self.db = db
    def get(self): return self.db.scalar(select(FooterConfiguration).limit(1))
    def list(self, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        filters = []
        if is_active is not None: filters.append(FooterConfiguration.is_active == is_active)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(FooterConfiguration).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(FooterConfiguration).where(*filters)) or 0
    def get_by_uuid(self, uuid: str): return self.db.scalar(select(FooterConfiguration).where(FooterConfiguration.uuid == uuid))
    def save(self, item: FooterConfiguration, values: dict):
        for field, value in values.items(): setattr(item, field, value)
        self.db.add(item); self.db.commit(); self.db.refresh(item); return item
    def delete(self, item: FooterConfiguration) -> None:
        self.db.delete(item); self.db.commit()
