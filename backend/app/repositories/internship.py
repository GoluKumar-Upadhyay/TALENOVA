"""Internship persistence layer."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.internship import InternshipProgram
class InternshipRepository:
    """Database operations for internships."""
    def __init__(self, db: Session) -> None: self.db = db
    SORT_FIELDS = {"title": InternshipProgram.title, "company": InternshipProgram.company, "display_order": InternshipProgram.display_order, "created_at": InternshipProgram.created_at}
    def list(self, search: str | None, internship_type: str | None, featured: bool | None, coming_soon: bool | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[InternshipProgram], int]:
        filters = [InternshipProgram.is_deleted.is_(False)]
        if search: filters.append(InternshipProgram.title.ilike(f"%{search}%"))
        if internship_type: filters.append(InternshipProgram.internship_type == internship_type)
        if featured is not None: filters.append(InternshipProgram.is_featured == featured)
        if coming_soon is not None: filters.append(InternshipProgram.is_coming_soon == coming_soon)
        if is_active is not None: filters.append(InternshipProgram.is_active == is_active)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(InternshipProgram).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(InternshipProgram).where(*filters)) or 0
    def get(self, uuid: str) -> InternshipProgram | None: return self.db.scalar(select(InternshipProgram).where(InternshipProgram.uuid == uuid, InternshipProgram.is_deleted.is_(False)))
    def save(self, item: InternshipProgram, values: dict) -> InternshipProgram:
        for field, value in values.items(): setattr(item, field, value)
        self.db.add(item); self.db.commit(); self.db.refresh(item); return item
