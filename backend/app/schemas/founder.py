"""Founder API contracts."""

from typing import Literal
from pydantic import BaseModel, Field


class FounderWrite(BaseModel):
    """Validated founder CMS payload."""

    founder_type: Literal["founder", "co_founder"]
    name: str = Field(min_length=2, max_length=180)
    bio: str | None = Field(default=None, max_length=30000)
    photo_url: str | None = Field(default=None, max_length=1000)
    education: list[dict] = Field(default_factory=list)
    experience: list[dict] = Field(default_factory=list)
    research: list[dict] = Field(default_factory=list)
    achievements: list[dict] = Field(default_factory=list)
    social_links: dict[str, str] = Field(default_factory=dict)
    resume_url: str | None = Field(default=None, max_length=1000)
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True


class FounderRead(FounderWrite):
    """Founder response payload."""

    uuid: str


class FounderPage(BaseModel):
    """Paginated founder response."""

    items: list[FounderRead]
    total: int
    page: int
    page_size: int
