"""Teacher business operations."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.teacher import TeacherRepository


class TeacherService:
    """Coordinates teacher validation and persistence."""
    SORT_FIELDS = set(TeacherRepository.SORT_FIELDS)

    def __init__(self, db: Session) -> None:
        self.repository = TeacherRepository(db)

    def list(self, search: str | None, designation: str | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        """List searchable public or administrative teacher records."""
        if sort not in self.SORT_FIELDS:
            raise HTTPException(status_code=422, detail="Unsupported teacher sort field")
        if direction not in {"asc", "desc"}:
            raise HTTPException(status_code=422, detail="Unsupported sort direction")
        return self.repository.list(search, designation, is_active, sort, direction, page, page_size)

    def get(self, uuid: str):
        teacher = self.repository.get(uuid)
        if teacher is None:
            raise HTTPException(status_code=404, detail="Teacher not found")
        return teacher

    def create(self, values: dict):
        """Create a teacher with normalized unique skill labels."""

        values["skills"] = sorted(set(skill.strip() for skill in values["skills"] if skill.strip()))
        return self.repository.create(values)

    def update(self, uuid: str, values: dict):
        """Update an existing teacher or report a missing profile."""

        teacher = self.get(uuid)
        values["skills"] = sorted(set(skill.strip() for skill in values["skills"] if skill.strip()))
        return self.repository.update(teacher, values)

    def delete(self, uuid: str) -> None:
        """Soft-delete a teacher profile."""

        teacher = self.get(uuid)
        self.repository.update(teacher, {"is_deleted": True})
