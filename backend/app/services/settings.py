"""Website settings business operations."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.settings import WebsiteSettings
from app.repositories.settings import SettingsRepository
class SettingsService:
    """Reads and updates the settings singleton."""
    SORT_FIELDS = set(SettingsRepository.SORT_FIELDS)
    def __init__(self, db: Session) -> None: self.repository = SettingsRepository(db)
    def list(self, maintenance_mode: bool | None, sort: str, direction: str, page: int, page_size: int):
        if sort not in self.SORT_FIELDS: raise HTTPException(422, "Unsupported settings sort field")
        if direction not in {"asc", "desc"}: raise HTTPException(422, "Unsupported sort direction")
        return self.repository.list(maintenance_mode, sort, direction, page, page_size)
    def get(self):
        item = self.repository.get()
        if item is None: raise HTTPException(404, "Website settings not found")
        return item
    def get_by_uuid(self, uuid: str):
        item = self.repository.get_by_uuid(uuid)
        if item is None: raise HTTPException(404, "Website settings not found")
        return item
    def create(self, values: dict): return self.repository.save(WebsiteSettings(**values), {})
    def save(self, values: dict):
        item = self.repository.get()
        return self.repository.save(item or WebsiteSettings(**values), values)
    def update(self, uuid: str, values: dict): return self.repository.save(self.get_by_uuid(uuid), values)
    def delete(self, uuid: str) -> None: self.repository.delete(self.get_by_uuid(uuid))
