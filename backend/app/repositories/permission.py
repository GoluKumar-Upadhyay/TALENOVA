"""Database access implementation for permission records."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.auth import Permission


class PermissionRepository:
    """Encapsulates query behavior for permissions."""

    SORT_FIELDS = {
        "code": Permission.code,
        "name": Permission.name,
        "created_at": Permission.created_at,
        "updated_at": Permission.updated_at,
    }

    def __init__(self, db: Session) -> None:
        self.db = db

    def list(
        self,
        search: str | None,
        is_active: bool | None,
        sort: str,
        direction: str,
        page: int,
        page_size: int,
    ) -> tuple[list[Permission], int]:
        filters = [Permission.is_deleted.is_(False)]
        if search:
            like = f"%{search}%"
            filters.append(Permission.code.ilike(like) | Permission.name.ilike(like))
        if is_active is not None:
            filters.append(Permission.is_active == is_active)
        order_column = self.SORT_FIELDS[sort]
        order_by = order_column.desc() if direction == "desc" else order_column.asc()
        query = select(Permission).where(*filters).order_by(order_by)
        items = list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size)))
        total = self.db.scalar(select(func.count()).select_from(Permission).where(*filters))
        return items, total or 0

    def get(self, uuid: str) -> Permission | None:
        return self.db.scalar(select(Permission).where(Permission.uuid == uuid, Permission.is_deleted.is_(False)))

    def get_by_code(self, code: str) -> Permission | None:
        return self.db.scalar(select(Permission).where(Permission.code == code, Permission.is_deleted.is_(False)))

    def get_many(self, uuids: list[str]) -> list[Permission]:
        if not uuids:
            return []
        return list(
            self.db.scalars(select(Permission).where(Permission.uuid.in_(uuids), Permission.is_deleted.is_(False)))
        )

    def create(self, values: dict) -> Permission:
        item = Permission(**values)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: Permission, values: dict) -> Permission:
        for field, value in values.items():
            setattr(item, field, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: Permission) -> None:
        item.is_deleted = True
        self.db.commit()
