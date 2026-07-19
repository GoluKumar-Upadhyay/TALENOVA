"""Navigation business rules."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.navigation import NavigationItem
from app.repositories.navigation import NavigationRepository
class NavigationService:
    """Validates menu links and hierarchy."""
    SORT_FIELDS = set(NavigationRepository.SORT_FIELDS)
    def __init__(self, db: Session) -> None: self.repository = NavigationRepository(db)
    def list(self, location: str | None, search: str | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        if sort not in self.SORT_FIELDS: raise HTTPException(422, "Unsupported navigation sort field")
        if direction not in {"asc", "desc"}: raise HTTPException(422, "Unsupported sort direction")
        return self.repository.list(location, search, is_active, sort, direction, page, page_size)
    def get(self, uuid: str): return self._get(uuid)
    def create(self, values: dict):
        self._validate(values); return self.repository.save(NavigationItem(**values), {})
    def update(self, uuid: str, values: dict):
        item = self._get(uuid); self._validate(values); return self.repository.save(item, values)
    def delete(self, uuid: str) -> None:
        self.repository.delete(self._get(uuid))
    def _get(self, uuid: str):
        item = self.repository.get(uuid)
        if item is None: raise HTTPException(404, "Navigation item not found")
        return item
    @staticmethod
    def _validate(values: dict) -> None:
        location = values.get("location", "header")
        if location not in {"header", "footer", "mobile"}: raise HTTPException(422, "Invalid menu location")
        if values.get("is_external") and not values["href"].startswith(("http://", "https://")): raise HTTPException(422, "External links require an absolute URL")
