"""Role business operations."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.permission import PermissionRepository
from app.repositories.role import RoleRepository


class RoleService:
    """Coordinates role validation, permissions, and persistence."""

    SORT_FIELDS = {"name", "created_at", "updated_at"}
    SORT_DIRECTIONS = {"asc", "desc"}

    def __init__(self, db: Session) -> None:
        self.repository = RoleRepository(db)
        self.permission_repository = PermissionRepository(db)

    def list(
        self,
        search: str | None,
        is_active: bool | None,
        permission_code: str | None,
        sort: str,
        direction: str,
        page: int,
        page_size: int,
    ):
        self._validate_sort(sort, direction)
        return self.repository.list(search, is_active, permission_code, sort, direction, page, page_size)

    def get(self, uuid: str):
        role = self.repository.get(uuid)
        if role is None:
            raise HTTPException(status_code=404, detail="Role not found")
        return role

    def create(self, values: dict):
        permission_uuids = values.pop("permission_uuids", [])
        if self.repository.get_by_name(values["name"]):
            raise HTTPException(status_code=409, detail="Role name already exists")
        permissions = self._permissions(permission_uuids)
        return self.repository.create(values, permissions)

    def update(self, uuid: str, values: dict):
        role = self.get(uuid)
        permission_uuids = values.pop("permission_uuids", None)
        values = {key: value for key, value in values.items() if value is not None}
        if "name" in values:
            existing = self.repository.get_by_name(values["name"])
            if existing and existing.uuid != uuid:
                raise HTTPException(status_code=409, detail="Role name already exists")
        permissions = self._permissions(permission_uuids) if permission_uuids is not None else None
        return self.repository.update(role, values, permissions)

    def delete(self, uuid: str) -> None:
        self.repository.delete(self.get(uuid))

    def attach_permission(self, role_uuid: str, permission_uuid: str):
        role = self.get(role_uuid)
        permission = self.permission_repository.get(permission_uuid)
        if permission is None:
            raise HTTPException(status_code=404, detail="Permission not found")
        if permission not in role.permissions:
            role.permissions.append(permission)
        self.repository.db.commit()
        return self.repository.get(role.uuid)

    def detach_permission(self, role_uuid: str, permission_uuid: str):
        role = self.get(role_uuid)
        permission = self.permission_repository.get(permission_uuid)
        if permission is None:
            raise HTTPException(status_code=404, detail="Permission not found")
        role.permissions = [item for item in role.permissions if item.uuid != permission_uuid]
        self.repository.db.commit()
        return self.repository.get(role.uuid)

    def _permissions(self, permission_uuids: list[str]) -> list:
        permissions = self.permission_repository.get_many(permission_uuids)
        if len(permissions) != len(set(permission_uuids)):
            raise HTTPException(status_code=422, detail="One or more permissions do not exist")
        return permissions

    def _validate_sort(self, sort: str, direction: str) -> None:
        if sort not in self.SORT_FIELDS:
            raise HTTPException(status_code=422, detail="Unsupported role sort field")
        if direction not in self.SORT_DIRECTIONS:
            raise HTTPException(status_code=422, detail="Unsupported sort direction")
