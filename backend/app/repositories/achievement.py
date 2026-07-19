"""Achievement persistence operations."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.achievement import Achievement
class AchievementRepository:
    """Database queries for achievement records."""
    def __init__(self, db: Session) -> None: self.db = db
    SORT_FIELDS = {"title": Achievement.title, "display_order": Achievement.display_order, "created_at": Achievement.created_at}
    def list(self, search: str | None, achievement_type: str | None, featured: bool | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[Achievement], int]:
        """List searchable non-deleted achievements."""
        filters = [Achievement.is_deleted.is_(False)]
        if search: filters.append(Achievement.title.ilike(f"%{search}%"))
        if achievement_type: filters.append(Achievement.achievement_type == achievement_type)
        if featured is not None: filters.append(Achievement.is_featured == featured)
        if is_active is not None: filters.append(Achievement.is_active == is_active)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(Achievement).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(Achievement).where(*filters)) or 0
    def get(self, uuid: str) -> Achievement | None: return self.db.scalar(select(Achievement).where(Achievement.uuid == uuid, Achievement.is_deleted.is_(False)))
    def save(self, item: Achievement, values: dict) -> Achievement:
        for field, value in values.items(): setattr(item, field, value)
        self.db.add(item); self.db.commit(); self.db.refresh(item); return item
