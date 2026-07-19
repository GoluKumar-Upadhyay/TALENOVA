"""Success story persistence operations."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.success_story import SuccessStory
class SuccessStoryRepository:
    """Database queries for success stories."""
    def __init__(self, db: Session) -> None: self.db = db
    SORT_FIELDS = {"name": SuccessStory.name, "display_order": SuccessStory.display_order, "created_at": SuccessStory.created_at, "graduation_year": SuccessStory.graduation_year}
    def list(self, search: str | None, featured: bool | None, is_active: bool | None, course: str | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[SuccessStory], int]:
        """List searchable non-deleted stories."""
        filters = [SuccessStory.is_deleted.is_(False)]
        if search: filters.append(SuccessStory.name.ilike(f"%{search}%"))
        if featured is not None: filters.append(SuccessStory.is_featured == featured)
        if is_active is not None: filters.append(SuccessStory.is_active == is_active)
        if course: filters.append(SuccessStory.course == course)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(SuccessStory).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(SuccessStory).where(*filters)) or 0
    def get(self, uuid: str) -> SuccessStory | None: return self.db.scalar(select(SuccessStory).where(SuccessStory.uuid == uuid, SuccessStory.is_deleted.is_(False)))
    def save(self, item: SuccessStory, values: dict) -> SuccessStory:
        for key, value in values.items(): setattr(item, key, value)
        self.db.add(item); self.db.commit(); self.db.refresh(item); return item
