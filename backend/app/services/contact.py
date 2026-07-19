"""Contact message business operations."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.contact import ContactRepository
class ContactService:
    """Coordinates validated inquiry workflows."""
    SORT_FIELDS = set(ContactRepository.SORT_FIELDS)
    def __init__(self, db: Session) -> None: self.repository = ContactRepository(db)
    def submit(self, values: dict):
        if values["contact_type"] == "college" and not values.get("organization"): raise HTTPException(422, "College name is required")
        return self.repository.create(values)
    def list(self, contact_type: str | None, status: str | None, is_read: bool | None, archived: bool | None, search: str | None, sort: str, direction: str, page: int, page_size: int):
        if sort not in self.SORT_FIELDS: raise HTTPException(422, "Unsupported contact sort field")
        if direction not in {"asc", "desc"}: raise HTTPException(422, "Unsupported sort direction")
        return self.repository.list(contact_type, status, is_read, archived, search, sort, direction, page, page_size)
    def get(self, uuid: str):
        item = self.repository.get(uuid)
        if item is None: raise HTTPException(404, "Contact message not found")
        return item
    def update(self, uuid: str, values: dict):
        return self.repository.save(self.get(uuid), values)
    def mark_read(self, uuid: str):
        item = self.get(uuid)
        return self.repository.save(item, {"is_read": True, "status": "read"})
    def set_status(self, uuid: str, status: str):
        item = self.get(uuid)
        return self.repository.save(item, {"status": status, "is_read": status != "new"})
    def delete(self, uuid: str):
        return self.repository.save(self.get(uuid), {"is_archived": True, "status": "archived"})
