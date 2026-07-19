"""Database access implementation for teacher records."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.teacher import Teacher


class TeacherRepository:
    """Encapsulates all ORM queries for teachers."""
    SORT_FIELDS = {"name": Teacher.name, "designation": Teacher.designation, "display_order": Teacher.display_order, "created_at": Teacher.created_at}

    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, search: str | None, designation: str | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[Teacher], int]:
        """Return soft-delete filtered teachers and their total count."""

        filters = [Teacher.is_deleted.is_(False)]
        if search:
            filters.append(Teacher.name.ilike(f"%{search}%"))
        if designation:
            filters.append(Teacher.designation.ilike(f"%{designation}%"))
        if is_active is not None:
            filters.append(Teacher.is_active == is_active)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(Teacher).where(*filters).order_by(order)
        items = list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size)))
        total = self.db.scalar(select(func.count()).select_from(Teacher).where(*filters))
        return items, total or 0

    def get(self, uuid: str) -> Teacher | None:
        """Get one non-deleted teacher by public identifier."""

        return self.db.scalar(select(Teacher).where(Teacher.uuid == uuid, Teacher.is_deleted.is_(False)))

    def create(self, values: dict) -> Teacher:
        """Create and persist a teacher profile."""

        teacher = Teacher(**values)
        self.db.add(teacher)
        self.db.commit()
        self.db.refresh(teacher)
        return teacher

    def update(self, teacher: Teacher, values: dict) -> Teacher:
        """Apply a validated mutation to a teacher profile."""

        for field, value in values.items():
            setattr(teacher, field, value)
        self.db.commit()
        self.db.refresh(teacher)
        return teacher
