"""Database access implementation for role records."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.auth import Permission, Role


class RoleRepository:
    """Encapsulates query behavior for roles."""

    SORT_FIELDS = {
        "name": Role.name,
        "created_at": Role.created_at,
        "updated_at": Role.updated_at,
    }

    def __init__(self, db: Session) -> None:
        self.db = db

    def list(
        self,
        search: str | None,
        is_active: bool | None,
        permission_code: str | None,
        sort: str,
        direction: str,
        page: int,
        page_size: int,
    ) -> tuple[list[Role], int]:
        filters = [Role.is_deleted.is_(False)]
        if search:
            filters.append(Role.name.ilike(f"%{search}%"))
        if is_active is not None:
            filters.append(Role.is_active == is_active)
        query = select(Role).options(selectinload(Role.permissions)).where(*filters)
        count_query = select(func.count(func.distinct(Role.id))).select_from(Role).where(*filters)
        if permission_code:
            query = query.join(Role.permissions).where(Permission.code == permission_code)
            count_query = count_query.join(Role.permissions).where(Permission.code == permission_code)
        order_column = self.SORT_FIELDS[sort]
        order_by = order_column.desc() if direction == "desc" else order_column.asc()
        query = query.order_by(order_by).offset((page - 1) * page_size).limit(page_size)
        items = list(self.db.scalars(query).unique())
        total = self.db.scalar(count_query)
        return items, total or 0

    def get(self, uuid: str) -> Role | None:
        return self.db.scalar(
            select(Role).options(selectinload(Role.permissions)).where(Role.uuid == uuid, Role.is_deleted.is_(False))
        )

    def get_by_name(self, name: str) -> Role | None:
        return self.db.scalar(select(Role).where(Role.name == name, Role.is_deleted.is_(False)))

    def get_many(self, uuids: list[str]) -> list[Role]:
        if not uuids:
            return []
        return list(
            self.db.scalars(
                select(Role).options(selectinload(Role.permissions)).where(Role.uuid.in_(uuids), Role.is_deleted.is_(False))
            ).unique()
        )

    def create(self, values: dict, permissions: list[Permission]) -> Role:
        role = Role(**values)
        role.permissions = permissions
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return self.get(role.uuid) or role

    def update(self, role: Role, values: dict, permissions: list[Permission] | None = None) -> Role:
        for field, value in values.items():
            setattr(role, field, value)
        if permissions is not None:
            role.permissions = permissions
        self.db.commit()
        self.db.refresh(role)
        return self.get(role.uuid) or role

    def delete(self, role: Role) -> None:
        role.is_deleted = True
        self.db.commit()
