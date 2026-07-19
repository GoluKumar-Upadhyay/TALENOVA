"""Video database access operations."""

from __future__ import annotations
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.video import Video

class VideoRepository:
    """Encapsulates queries for workshop video records."""
    SORT_FIELDS = {"title": Video.title, "category": Video.category, "display_order": Video.display_order, "created_at": Video.created_at, "duration_seconds": Video.duration_seconds}
    def __init__(self, db: Session) -> None:
        self.db = db
    def list(self, search: str | None, category: str | None, featured: bool | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[Video], int]:
        """List videos with filters and pagination."""
        filters = [Video.is_deleted.is_(False)]
        if search: filters.append(Video.title.ilike(f"%{search}%"))
        if category: filters.append(Video.category == category)
        if featured is not None: filters.append(Video.is_featured == featured)
        if is_active is not None: filters.append(Video.is_active == is_active)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(Video).where(*filters).order_by(order)
        items = list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size)))
        total = self.db.scalar(select(func.count()).select_from(Video).where(*filters)) or 0
        return items, total
    def get(self, uuid: str) -> Video | None:
        """Find a video by public identifier."""
        return self.db.scalar(select(Video).where(Video.uuid == uuid, Video.is_deleted.is_(False)))
    def create(self, values: dict) -> Video:
        """Create a video record."""
        item = Video(**values); self.db.add(item); self.db.commit(); self.db.refresh(item); return item
    def save(self, item: Video, values: dict) -> Video:
        """Persist a video update."""
        for field, value in values.items(): setattr(item, field, value)
        self.db.commit(); self.db.refresh(item); return item
