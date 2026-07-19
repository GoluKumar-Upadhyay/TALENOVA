"""FAQ database operations."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.faq import FAQ
class FAQRepository:
    """Persistence queries for FAQs."""
    def __init__(self, db: Session) -> None: self.db = db
    SORT_FIELDS = {"question": FAQ.question, "display_order": FAQ.display_order, "created_at": FAQ.created_at, "category": FAQ.category}
    def list(self, search: str | None, page_key: str | None, category: str | None, featured: bool | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[FAQ], int]:
        filters = [FAQ.is_deleted.is_(False)]
        if search: filters.append(FAQ.question.ilike(f"%{search}%"))
        if page_key: filters.append(FAQ.page == page_key)
        if category: filters.append(FAQ.category == category)
        if featured is not None: filters.append(FAQ.is_featured == featured)
        if is_active is not None: filters.append(FAQ.is_active == is_active)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(FAQ).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(FAQ).where(*filters)) or 0
    def get(self, uuid: str) -> FAQ | None: return self.db.scalar(select(FAQ).where(FAQ.uuid == uuid, FAQ.is_deleted.is_(False)))
    def save(self, item: FAQ, values: dict) -> FAQ:
        for field, value in values.items(): setattr(item, field, value)
        self.db.add(item); self.db.commit(); self.db.refresh(item); return item
