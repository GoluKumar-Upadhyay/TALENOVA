"""FAQ business workflows."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.faq import FAQ
from app.repositories.faq import FAQRepository
class FAQService:
    """Coordinates FAQ lifecycle operations."""
    def __init__(self, db: Session) -> None: self.repository = FAQRepository(db)
    SORT_FIELDS = set(FAQRepository.SORT_FIELDS)
    def list(self, search: str | None, page_key: str | None, category: str | None, featured: bool | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        if sort not in self.SORT_FIELDS: raise HTTPException(422, "Unsupported FAQ sort field")
        if direction not in {"asc", "desc"}: raise HTTPException(422, "Unsupported sort direction")
        return self.repository.list(search, page_key, category, featured, is_active, sort, direction, page, page_size)
    def get(self, uuid: str): return self._get(uuid)
    def create(self, values: dict): return self.repository.save(FAQ(**values), {})
    def update(self, uuid: str, values: dict): return self.repository.save(self._get(uuid), values)
    def delete(self, uuid: str): return self.repository.save(self._get(uuid), {"is_deleted": True})
    def _get(self, uuid: str) -> FAQ:
        item = self.repository.get(uuid)
        if item is None: raise HTTPException(404, "FAQ not found")
        return item
