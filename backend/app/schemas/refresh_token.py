"""Refresh token API validation and representation contracts."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class RefreshTokenRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: str
    user_uuid: str
    user_email: EmailStr
    expires_at: datetime
    revoked_at: datetime | None
    is_active: bool
    is_expired: bool


class RefreshTokenPage(BaseModel):
    items: list[RefreshTokenRead]
    total: int
    page: int
    page_size: int
