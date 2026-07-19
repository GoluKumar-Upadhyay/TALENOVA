"""Footer business operations."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.footer import FooterConfiguration
from app.repositories.footer import FooterRepository
class FooterService:
    """Coordinates footer singleton updates."""
    SORT_FIELDS = set(FooterRepository.SORT_FIELDS)
    def __init__(self, db: Session) -> None: self.repository = FooterRepository(db)
    def list(self, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        if sort not in self.SORT_FIELDS: raise HTTPException(422, "Unsupported footer sort field")
        if direction not in {"asc", "desc"}: raise HTTPException(422, "Unsupported sort direction")
        return self.repository.list(is_active, sort, direction, page, page_size)
    def get(self):
        item = self.repository.get()
        if item is None: raise HTTPException(404, "Footer configuration not found")
        return item
    def get_by_uuid(self, uuid: str):
        item = self.repository.get_by_uuid(uuid)
        if item is None: raise HTTPException(404, "Footer configuration not found")
        return item
    def create(self, values: dict): return self.repository.save(FooterConfiguration(**values), {})
    def save(self, values: dict):
        item = self.repository.get()
        return self.repository.save(item or FooterConfiguration(**values), values)
    def update(self, uuid: str, values: dict): return self.repository.save(self.get_by_uuid(uuid), values)
    def delete(self, uuid: str) -> None: self.repository.delete(self.get_by_uuid(uuid))
