"""Database access implementation for user records."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.auth import Role, User


class UserRepository:
    """Encapsulates query behavior for users."""

    SORT_FIELDS = {
        "email": User.email,
        "full_name": User.full_name,
        "created_at": User.created_at,
        "updated_at": User.updated_at,
        "last_login_at": User.last_login_at,
    }

    def __init__(self, db: Session) -> None:
        self.db = db

    def list(
        self,
        search: str | None,
        role: str | None,
        is_active: bool | None,
        is_email_verified: bool | None,
        sort: str,
        direction: str,
        page: int,
        page_size: int,
    ) -> tuple[list[User], int]:
        filters = [User.is_deleted.is_(False)]
        if search:
            like = f"%{search}%"
            filters.append(User.email.ilike(like) | User.full_name.ilike(like))
        if is_active is not None:
            filters.append(User.is_active == is_active)
        if is_email_verified is not None:
            filters.append(User.is_email_verified == is_email_verified)
        query = select(User).options(selectinload(User.roles).selectinload(Role.permissions)).where(*filters)
        count_query = select(func.count(func.distinct(User.id))).select_from(User).where(*filters)
        if role:
            query = query.join(User.roles).where(Role.name == role)
            count_query = count_query.join(User.roles).where(Role.name == role)
        order_column = self.SORT_FIELDS[sort]
        order_by = order_column.desc() if direction == "desc" else order_column.asc()
        query = query.order_by(order_by).offset((page - 1) * page_size).limit(page_size)
        items = list(self.db.scalars(query).unique())
        total = self.db.scalar(count_query)
        return items, total or 0

    def get(self, uuid: str) -> User | None:
        return self.db.scalar(
            select(User).options(selectinload(User.roles).selectinload(Role.permissions)).where(
                User.uuid == uuid,
                User.is_deleted.is_(False),
            )
        )

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(
            select(User).options(selectinload(User.roles).selectinload(Role.permissions)).where(
                User.email == email,
                User.is_deleted.is_(False),
            )
        )

    def create(self, values: dict, roles: list[Role]) -> User:
        user = User(**values)
        user.roles = roles
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return self.get(user.uuid) or user

    def update(self, user: User, values: dict, roles: list[Role] | None = None) -> User:
        for field, value in values.items():
            setattr(user, field, value)
        if roles is not None:
            user.roles = roles
        self.db.commit()
        self.db.refresh(user)
        return self.get(user.uuid) or user

    def delete(self, user: User) -> None:
        user.is_deleted = True
        self.db.commit()
