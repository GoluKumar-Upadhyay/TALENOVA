"""Founder profile business operations."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.founder import FounderRepository


class FounderService:
    """Coordinates founder validation and persistence workflows."""
    SORT_FIELDS = set(FounderRepository.SORT_FIELDS)

    def __init__(self, db: Session) -> None:
        self.repository = FounderRepository(db)

    def list_public(self):
        """Return visible founder profiles for public rendering."""

        return self.repository.list_active()

    def list(self, search: str | None, founder_type: str | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        if sort not in self.SORT_FIELDS:
            raise HTTPException(422, "Unsupported founder sort field")
        if direction not in {"asc", "desc"}:
            raise HTTPException(422, "Unsupported sort direction")
        return self.repository.list(search, founder_type, is_active, sort, direction, page, page_size)

    def get(self, uuid: str):
        item = self.repository.get(uuid)
        if item is None:
            raise HTTPException(404, "Founder profile not found")
        return item

    def create(self, values: dict):
        if self.repository.get_by_type(values["founder_type"]):
            raise HTTPException(409, "Founder type already exists")
        return self.repository.create(values)

    def update(self, uuid: str, values: dict):
        existing = self.repository.get_by_type(values["founder_type"])
        if existing and existing.uuid != uuid:
            raise HTTPException(409, "Founder type already exists")
        return self.repository.update(self.get(uuid), values)

    def delete(self, uuid: str):
        return self.repository.update(self.get(uuid), {"is_deleted": True})

    def save(self, founder_type: str, values: dict):
        """Create or update the unique profile for a leadership type."""

        if founder_type != values["founder_type"]:
            raise ValueError("Founder type must match the URL path")
        existing = self.repository.get_by_type(founder_type)
        if existing is None:
            return self.repository.create(values)
        return self.repository.update(existing, values)
