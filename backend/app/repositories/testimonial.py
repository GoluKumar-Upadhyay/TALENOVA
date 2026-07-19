"""Testimonial database access."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.testimonial import Testimonial
class TestimonialRepository:
    """Persistence access for testimonials."""
    def __init__(self, db: Session) -> None: self.db = db
    SORT_FIELDS = {"student_name": Testimonial.student_name, "rating": Testimonial.rating, "display_order": Testimonial.display_order, "created_at": Testimonial.created_at}
    def list(self, search: str | None, featured: bool | None, is_active: bool | None, min_rating: int | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[Testimonial], int]:
        """Find visible testimonials."""
        filters = [Testimonial.is_deleted.is_(False)]
        if search: filters.append(Testimonial.student_name.ilike(f"%{search}%"))
        if featured is not None: filters.append(Testimonial.is_featured == featured)
        if is_active is not None: filters.append(Testimonial.is_active == is_active)
        if min_rating is not None: filters.append(Testimonial.rating >= min_rating)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(Testimonial).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(Testimonial).where(*filters)) or 0
    def get(self, uuid: str) -> Testimonial | None: return self.db.scalar(select(Testimonial).where(Testimonial.uuid == uuid, Testimonial.is_deleted.is_(False)))
    def save(self, item: Testimonial, values: dict) -> Testimonial:
        for key, value in values.items(): setattr(item, key, value)
        self.db.add(item); self.db.commit(); self.db.refresh(item); return item
