"""Role API validation and representation contracts."""

import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.permission import PermissionRead


class RoleWrite(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    description: str | None = Field(default=None, max_length=2000)
    permission_uuids: list[str] = Field(default_factory=list)
    is_active: bool = True

    @field_validator("name")
    @classmethod
    def role_name(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not re.fullmatch(r"[a-z][a-z0-9_-]*", normalized):
            raise ValueError("Role name may contain lowercase letters, numbers, underscores, and dashes")
        return normalized


class RoleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    description: str | None = Field(default=None, max_length=2000)
    permission_uuids: list[str] | None = None
    is_active: bool | None = None

    @field_validator("name")
    @classmethod
    def role_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().lower()
        if not re.fullmatch(r"[a-z][a-z0-9_-]*", normalized):
            raise ValueError("Role name may contain lowercase letters, numbers, underscores, and dashes")
        return normalized


class RoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: str
    name: str
    description: str | None
    permissions: list[PermissionRead]
    is_active: bool


class RolePage(BaseModel):
    items: list[RoleRead]
    total: int
    page: int
    page_size: int
