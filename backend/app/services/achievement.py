"""Achievement business operations."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.achievement import Achievement
from app.repositories.achievement import AchievementRepository
class AchievementService:
    """Coordinates achievement lifecycle operations."""
    def __init__(self, db: Session) -> None: self.repository = AchievementRepository(db)
    SORT_FIELDS = set(AchievementRepository.SORT_FIELDS)
    def list(self, search: str | None, achievement_type: str | None, featured: bool | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        if sort not in self.SORT_FIELDS: raise HTTPException(422, "Unsupported achievement sort field")
        if direction not in {"asc", "desc"}: raise HTTPException(422, "Unsupported sort direction")
        return self.repository.list(search, achievement_type, featured, is_active, sort, direction, page, page_size)
    def get(self, uuid: str): return self._get(uuid)
    def create(self, values: dict): return self.repository.save(Achievement(**values), {})
    def update(self, uuid: str, values: dict): return self.repository.save(self._get(uuid), values)
    def delete(self, uuid: str) -> None: self.repository.save(self._get(uuid), {"is_deleted": True})
    def _get(self, uuid: str) -> Achievement:
        item = self.repository.get(uuid)
        if item is None: raise HTTPException(status_code=404, detail="Achievement not found")
        return item
