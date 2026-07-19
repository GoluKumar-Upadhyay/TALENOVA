"""SEO business operations."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.seo import SEORecord
from app.repositories.seo import SEORepository
class SEOService:
    """Coordinates page metadata persistence."""
    SORT_FIELDS = set(SEORepository.SORT_FIELDS)
    def __init__(self, db: Session) -> None: self.repository = SEORepository(db)
    def list(self, search: str | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        if sort not in self.SORT_FIELDS: raise HTTPException(422, "Unsupported SEO sort field")
        if direction not in {"asc", "desc"}: raise HTTPException(422, "Unsupported sort direction")
        return self.repository.list(search, is_active, sort, direction, page, page_size)
    def get(self, page_key: str):
        item = self.repository.get(page_key)
        if item is None: raise HTTPException(404, "SEO record not found")
        return item
    def get_by_uuid(self, uuid: str):
        item = self.repository.get_by_uuid(uuid)
        if item is None: raise HTTPException(404, "SEO record not found")
        return item
    def create(self, values: dict):
        if self.repository.get(values["page_key"]): raise HTTPException(409, "SEO page key already exists")
        return self.repository.save(SEORecord(**values), {})
    def save(self, values: dict):
        item = self.repository.get(values["page_key"])
        return self.repository.save(item or SEORecord(**values), values)
    def update(self, uuid: str, values: dict):
        item = self.get_by_uuid(uuid)
        existing = self.repository.get(values["page_key"])
        if existing and existing.uuid != uuid: raise HTTPException(409, "SEO page key already exists")
        return self.repository.save(item, values)
    def delete(self, uuid: str) -> None: self.repository.delete(self.get_by_uuid(uuid))
