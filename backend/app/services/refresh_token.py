"""Refresh token administrative operations."""

from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.auth import RefreshToken
from app.repositories.refresh_token import RefreshTokenRepository


class RefreshTokenService:
    """Coordinates refresh token listing and revocation."""

    SORT_FIELDS = {"created_at", "expires_at", "revoked_at"}
    SORT_DIRECTIONS = {"asc", "desc"}
    STATUSES = {None, "active", "revoked", "expired"}

    def __init__(self, db: Session) -> None:
        self.repository = RefreshTokenRepository(db)

    def list(
        self,
        search: str | None,
        user_uuid: str | None,
        status: str | None,
        sort: str,
        direction: str,
        page: int,
        page_size: int,
    ):
        self._validate(search, status, sort, direction)
        return self.repository.list(search, user_uuid, status, sort, direction, page, page_size)

    def get(self, uuid: str):
        token = self.repository.get(uuid)
        if token is None:
            raise HTTPException(status_code=404, detail="Refresh token not found")
        return token

    def revoke(self, uuid: str):
        token = self.get(uuid)
        if token.revoked_at is None:
            token = self.repository.revoke(token)
        return token

    def serialize(self, token: RefreshToken) -> dict:
        return {
            "uuid": token.uuid,
            "user_uuid": token.user.uuid,
            "user_email": token.user.email,
            "expires_at": token.expires_at,
            "revoked_at": token.revoked_at,
            "is_active": token.revoked_at is None and token.expires_at > datetime.utcnow(),
            "is_expired": token.expires_at <= datetime.utcnow(),
        }

    def _validate(self, search: str | None, status: str | None, sort: str, direction: str) -> None:
        if search is not None and len(search.strip()) < 2:
            raise HTTPException(status_code=422, detail="Search must be at least 2 characters")
        if status not in self.STATUSES:
            raise HTTPException(status_code=422, detail="Unsupported refresh token status")
        if sort not in self.SORT_FIELDS:
            raise HTTPException(status_code=422, detail="Unsupported refresh token sort field")
        if direction not in self.SORT_DIRECTIONS:
            raise HTTPException(status_code=422, detail="Unsupported sort direction")
