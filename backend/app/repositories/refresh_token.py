"""Database access implementation for refresh token records."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.auth import RefreshToken, Role, User


class RefreshTokenRepository:
    """Encapsulates query behavior for refresh tokens."""

    SORT_FIELDS = {
        "created_at": RefreshToken.created_at,
        "expires_at": RefreshToken.expires_at,
        "revoked_at": RefreshToken.revoked_at,
    }

    def __init__(self, db: Session) -> None:
        self.db = db

    def list(
        self,
        search: str | None,
        user_uuid: str | None,
        status: str | None,
        sort: str,
        direction: str,
        page: int,
        page_size: int,
    ) -> tuple[list[RefreshToken], int]:
        now = datetime.utcnow()
        filters = [RefreshToken.is_deleted.is_(False)]
        query = select(RefreshToken).options(selectinload(RefreshToken.user)).join(RefreshToken.user).where(*filters)
        count_query = select(func.count()).select_from(RefreshToken).join(RefreshToken.user).where(*filters)
        if search:
            like = f"%{search}%"
            query = query.where(User.email.ilike(like))
            count_query = count_query.where(User.email.ilike(like))
        if user_uuid:
            query = query.where(User.uuid == user_uuid)
            count_query = count_query.where(User.uuid == user_uuid)
        if status == "active":
            query = query.where(RefreshToken.revoked_at.is_(None), RefreshToken.expires_at > now)
            count_query = count_query.where(RefreshToken.revoked_at.is_(None), RefreshToken.expires_at > now)
        elif status == "revoked":
            query = query.where(RefreshToken.revoked_at.is_not(None))
            count_query = count_query.where(RefreshToken.revoked_at.is_not(None))
        elif status == "expired":
            query = query.where(RefreshToken.expires_at <= now)
            count_query = count_query.where(RefreshToken.expires_at <= now)
        order_column = self.SORT_FIELDS[sort]
        order_by = order_column.desc() if direction == "desc" else order_column.asc()
        query = query.order_by(order_by).offset((page - 1) * page_size).limit(page_size)
        items = list(self.db.scalars(query).unique())
        total = self.db.scalar(count_query)
        return items, total or 0

    def get(self, uuid: str) -> RefreshToken | None:
        return self.db.scalar(
            select(RefreshToken)
            .options(selectinload(RefreshToken.user))
            .where(RefreshToken.uuid == uuid, RefreshToken.is_deleted.is_(False))
        )

    def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        return self.db.scalar(
            select(RefreshToken)
            .options(selectinload(RefreshToken.user).selectinload(User.roles).selectinload(Role.permissions))
            .where(RefreshToken.token_hash == token_hash, RefreshToken.is_deleted.is_(False))
        )

    def create(self, values: dict) -> RefreshToken:
        item = RefreshToken(**values)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def revoke(self, token: RefreshToken) -> RefreshToken:
        token.revoked_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(token)
        return token

    def revoke_for_user(self, user_id: int) -> int:
        active_tokens = list(
            self.db.scalars(
                select(RefreshToken).where(
                    RefreshToken.user_id == user_id,
                    RefreshToken.revoked_at.is_(None),
                    RefreshToken.is_deleted.is_(False),
                )
            )
        )
        now = datetime.utcnow()
        for token in active_tokens:
            token.revoked_at = now
        self.db.commit()
        return len(active_tokens)
