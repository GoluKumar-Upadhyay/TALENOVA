"""Reusable typed pagination, ordering, filtering, and slug helpers."""

import re
from math import ceil

from pydantic import BaseModel, Field


class PageParams(BaseModel):
    """Validated page parameters for all collection endpoints."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=24, ge=1, le=100)

    @property
    def offset(self) -> int:
        """Return the database offset for the selected page."""

        return (self.page - 1) * self.page_size


class PageMeta(BaseModel):
    """Metadata accompanying a paginated API collection."""

    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def create(cls, total: int, params: PageParams) -> "PageMeta":
        """Build pagination metadata from a total record count."""

        return cls(
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=ceil(total / params.page_size) if total else 0,
        )


def slugify(value: str) -> str:
    """Generate a URL-safe lowercase slug from user-supplied text."""

    slug = re.sub(r"[^a-z0-9]+", "-", value.lower().strip())
    return slug.strip("-")
