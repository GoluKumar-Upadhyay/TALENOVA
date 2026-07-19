"""User API validation and representation contracts."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.auth import validate_password_strength
from app.schemas.role import RoleRead


class UserWrite(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = Field(default=None, min_length=2, max_length=180)
    role_uuids: list[str] = Field(default_factory=list)
    is_active: bool = True
    is_email_verified: bool = False

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        return validate_password_strength(value)

    @field_validator("full_name")
    @classmethod
    def clean_name(cls, value: str | None) -> str | None:
        return value.strip() if value else value


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    full_name: str | None = Field(default=None, min_length=2, max_length=180)
    role_uuids: list[str] | None = None
    is_active: bool | None = None
    is_email_verified: bool | None = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str | None) -> str | None:
        return validate_password_strength(value) if value is not None else None

    @field_validator("full_name")
    @classmethod
    def clean_name(cls, value: str | None) -> str | None:
        return value.strip() if value else value


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: str
    email: EmailStr
    full_name: str | None
    is_active: bool
    is_email_verified: bool
    roles: list[RoleRead]


class UserPage(BaseModel):
    items: list[UserRead]
    total: int
    page: int
    page_size: int
