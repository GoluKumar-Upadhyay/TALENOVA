"""Success story business operations."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.success_story import SuccessStory
from app.repositories.success_story import SuccessStoryRepository
class SuccessStoryService:
    """Coordinates outcome story lifecycle operations."""
    def __init__(self, db: Session) -> None: self.repository = SuccessStoryRepository(db)
    SORT_FIELDS = set(SuccessStoryRepository.SORT_FIELDS)
    def list(self, search: str | None, featured: bool | None, is_active: bool | None, course: str | None, sort: str, direction: str, page: int, page_size: int):
        if sort not in self.SORT_FIELDS: raise HTTPException(status_code=422, detail="Unsupported success story sort field")
        if direction not in {"asc", "desc"}: raise HTTPException(status_code=422, detail="Unsupported sort direction")
        return self.repository.list(search, featured, is_active, course, sort, direction, page, page_size)
    def get(self, uuid: str): return self._find(uuid)
    def create(self, values: dict): return self.repository.save(SuccessStory(**values), {})
    def update(self, uuid: str, values: dict): return self.repository.save(self._find(uuid), values)
    def delete(self, uuid: str): self.repository.save(self._find(uuid), {"is_deleted": True})
    def _find(self, uuid: str) -> SuccessStory:
        item = self.repository.get(uuid)
        if item is None: raise HTTPException(status_code=404, detail="Success story not found")
        return item
