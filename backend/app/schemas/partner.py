"""Partner API contracts."""

from pydantic import BaseModel, Field


class PartnerWrite(BaseModel):
    """Validated partner CMS payload."""

    name: str = Field(min_length=2, max_length=255)
    website_url: str | None = Field(default=None, max_length=1000)
    logo_url: str | None = Field(default=None, max_length=1000)
    description: str | None = Field(default=None, max_length=10000)
    partner_type: str = Field(default="industry", min_length=2, max_length=80)
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True


class PartnerRead(PartnerWrite):
    """Partner response representation."""

    uuid: str


class PartnerPage(BaseModel):
    """Paginated partner collection response."""

    items: list[PartnerRead]
    total: int
    page: int
    page_size: int
