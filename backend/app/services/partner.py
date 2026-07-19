"""Partner business workflows."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.partner import PartnerRepository


class PartnerService:
    """Coordinates partner validation and persistence."""
    SORT_FIELDS = set(PartnerRepository.SORT_FIELDS)

    def __init__(self, db: Session) -> None:
        self.repository = PartnerRepository(db)

    def list(self, search: str | None, partner_type: str | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        """Return filtered partners."""
        if sort not in self.SORT_FIELDS:
            raise HTTPException(status_code=422, detail="Unsupported partner sort field")
        if direction not in {"asc", "desc"}:
            raise HTTPException(status_code=422, detail="Unsupported sort direction")
        return self.repository.list(search, partner_type, is_active, sort, direction, page, page_size)

    def get(self, uuid: str):
        item = self.repository.get(uuid)
        if item is None:
            raise HTTPException(status_code=404, detail="Partner not found")
        return item

    def create(self, values: dict):
        """Create a partner record."""

        return self.repository.create(values)

    def update(self, uuid: str, values: dict):
        """Update a partner record."""

        item = self.get(uuid)
        return self.repository.update(item, values)

    def delete(self, uuid: str) -> None:
        """Soft-delete a partner record."""

        item = self.get(uuid)
        self.repository.update(item, {"is_deleted": True})
