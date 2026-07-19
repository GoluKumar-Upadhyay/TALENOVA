"""Internship programme business operations."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.internship import InternshipProgram
from app.repositories.internship import InternshipRepository
class InternshipService:
    """Coordinates internship validation and persistence."""
    def __init__(self, db: Session) -> None: self.repository = InternshipRepository(db)
    SORT_FIELDS = set(InternshipRepository.SORT_FIELDS)
    def list(self, search: str | None, internship_type: str | None, featured: bool | None, coming_soon: bool | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        if sort not in self.SORT_FIELDS: raise HTTPException(422, "Unsupported internship sort field")
        if direction not in {"asc", "desc"}: raise HTTPException(422, "Unsupported sort direction")
        return self.repository.list(search, internship_type, featured, coming_soon, is_active, sort, direction, page, page_size)
    def get(self, uuid: str): return self._get(uuid)
    def create(self, values: dict): return self.repository.save(InternshipProgram(**values), {})
    def update(self, uuid: str, values: dict): return self.repository.save(self._get(uuid), values)
    def delete(self, uuid: str): self.repository.save(self._get(uuid), {"is_deleted": True})
    def _get(self, uuid: str) -> InternshipProgram:
        item = self.repository.get(uuid)
        if item is None: raise HTTPException(status_code=404, detail="Internship not found")
        return item
