"""Project business workflows."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.project import ProjectRepository
class ProjectService:
    """Coordinates project validation and persistence."""
    def __init__(self, db: Session) -> None: self.repository = ProjectRepository(db)
    SORT_FIELDS = set(ProjectRepository.SORT_FIELDS)
    def list(self, search: str | None, status: str | None, featured: bool | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        if sort not in self.SORT_FIELDS: raise HTTPException(status_code=422, detail="Unsupported project sort field")
        if direction not in {"asc", "desc"}: raise HTTPException(status_code=422, detail="Unsupported sort direction")
        return self.repository.list(search, status, featured, is_active, sort, direction, page, page_size)
    def get(self, uuid: str):
        item = self.repository.get(uuid)
        if item is None: raise HTTPException(status_code=404, detail="Project not found")
        return item
    def create(self, values: dict): return self.repository.create(self._normalize(values))
    def update(self, uuid: str, values: dict):
        item = self.get(uuid)
        return self.repository.save(item, self._normalize(values))
    def delete(self, uuid: str) -> None:
        item = self.get(uuid)
        self.repository.save(item, {"is_deleted": True})
    @staticmethod
    def _normalize(values: dict) -> dict:
        for field in ("technologies", "tags", "screenshot_urls"):
            values[field] = sorted(set(value.strip() for value in values[field] if value.strip()))
        return values
