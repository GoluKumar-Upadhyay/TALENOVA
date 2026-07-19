"""Testimonial operations."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.testimonial import Testimonial
from app.repositories.testimonial import TestimonialRepository
class TestimonialService:
    """Coordinates testimonial records."""
    def __init__(self, db: Session) -> None: self.repository = TestimonialRepository(db)
    SORT_FIELDS = set(TestimonialRepository.SORT_FIELDS)
    def list(self, search: str | None, featured: bool | None, is_active: bool | None, min_rating: int | None, sort: str, direction: str, page: int, page_size: int):
        if sort not in self.SORT_FIELDS: raise HTTPException(status_code=422, detail="Unsupported testimonial sort field")
        if direction not in {"asc", "desc"}: raise HTTPException(status_code=422, detail="Unsupported sort direction")
        return self.repository.list(search, featured, is_active, min_rating, sort, direction, page, page_size)
    def get(self, uuid: str): return self._get(uuid)
    def create(self, values: dict): return self.repository.save(Testimonial(**values), {})
    def update(self, uuid: str, values: dict): return self.repository.save(self._get(uuid), values)
    def delete(self, uuid: str): self.repository.save(self._get(uuid), {"is_deleted": True})
    def _get(self, uuid: str) -> Testimonial:
        item = self.repository.get(uuid)
        if item is None: raise HTTPException(status_code=404, detail="Testimonial not found")
        return item
