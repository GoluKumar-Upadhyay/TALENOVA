"""Permission business operations."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.permission import PermissionRepository


class PermissionService:
    """Coordinates permission validation and persistence."""

    SORT_FIELDS = {"code", "name", "created_at", "updated_at"}
    SORT_DIRECTIONS = {"asc", "desc"}

    def __init__(self, db: Session) -> None:
        self.repository = PermissionRepository(db)

    def list(
        self,
        search: str | None,
        is_active: bool | None,
        sort: str,
        direction: str,
        page: int,
        page_size: int,
    ):
        self._validate_sort(sort, direction)
        return self.repository.list(search, is_active, sort, direction, page, page_size)

    def get(self, uuid: str):
        item = self.repository.get(uuid)
        if item is None:
            raise HTTPException(status_code=404, detail="Permission not found")
        return item

    def create(self, values: dict):
        if self.repository.get_by_code(values["code"]):
            raise HTTPException(status_code=409, detail="Permission code already exists")
        return self.repository.create(values)

    def update(self, uuid: str, values: dict):
        item = self.get(uuid)
        values = {key: value for key, value in values.items() if value is not None}
        if "code" in values:
            existing = self.repository.get_by_code(values["code"])
            if existing and existing.uuid != uuid:
                raise HTTPException(status_code=409, detail="Permission code already exists")
        return self.repository.update(item, values)

    def delete(self, uuid: str) -> None:
        self.repository.delete(self.get(uuid))

    def _validate_sort(self, sort: str, direction: str) -> None:
        if sort not in self.SORT_FIELDS:
            raise HTTPException(status_code=422, detail="Unsupported permission sort field")
        if direction not in self.SORT_DIRECTIONS:
            raise HTTPException(status_code=422, detail="Unsupported sort direction")
