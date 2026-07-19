"""Navigation persistence layer."""

from __future__ import annotations
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.navigation import NavigationItem
class NavigationRepository:
    """Hierarchical menu queries and mutations."""
    SORT_FIELDS = {"label": NavigationItem.label, "location": NavigationItem.location, "display_order": NavigationItem.display_order, "created_at": NavigationItem.created_at}
    def __init__(self, db: Session) -> None: self.db = db
    def list(self, location: str | None, search: str | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[NavigationItem], int]:
        filters = []
        if location: filters.append(NavigationItem.location == location)
        if search: filters.append(NavigationItem.label.ilike(f"%{search}%"))
        if is_active is not None: filters.append(NavigationItem.is_active == is_active)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(NavigationItem).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(NavigationItem).where(*filters)) or 0
    def get(self, uuid: str) -> NavigationItem | None: return self.db.scalar(select(NavigationItem).where(NavigationItem.uuid == uuid))
    def save(self, item: NavigationItem, values: dict) -> NavigationItem:
        for field, value in values.items(): setattr(item, field, value)
        self.db.add(item); self.db.commit(); self.db.refresh(item); return item
    def delete(self, item: NavigationItem) -> None:
        self.db.delete(item); self.db.commit()
