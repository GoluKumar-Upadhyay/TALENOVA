"""Permission API validation and representation contracts."""

import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PermissionWrite(BaseModel):
    code: str = Field(min_length=3, max_length=120)
    name: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    is_active: bool = True

    @field_validator("code")
    @classmethod
    def permission_code(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not re.fullmatch(r"[a-z][a-z0-9_.-]*:[a-z][a-z0-9_.-]*", normalized):
            raise ValueError("Permission code must look like resource:action")
        return normalized

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        return value.strip()


class PermissionUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=3, max_length=120)
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    is_active: bool | None = None

    @field_validator("code")
    @classmethod
    def permission_code(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().lower()
        if not re.fullmatch(r"[a-z][a-z0-9_.-]*:[a-z][a-z0-9_.-]*", normalized):
            raise ValueError("Permission code must look like resource:action")
        return normalized


class PermissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: str
    code: str
    name: str
    description: str | None
    is_active: bool


class PermissionPage(BaseModel):
    items: list[PermissionRead]
    total: int
    page: int
    page_size: int
