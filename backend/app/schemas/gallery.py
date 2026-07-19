"""Gallery API contracts."""

from pydantic import BaseModel, ConfigDict, Field


class GalleryCategoryWrite(BaseModel):
    """Gallery category mutation payload."""
    name: str = Field(min_length=2, max_length=120)
    slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True


class GalleryImageWrite(BaseModel):
    """Gallery image mutation payload containing a stored media URL."""
    category_id: int = Field(gt=0)
    image_url: str = Field(min_length=1, max_length=1000)
    alt_text: str = Field(min_length=1, max_length=255)
    caption: str | None = Field(default=None, max_length=5000)
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True


class GalleryImageRead(GalleryImageWrite):
    """Public gallery image representation."""
    model_config = ConfigDict(from_attributes=True)

    uuid: str


class GalleryCategoryRead(GalleryCategoryWrite):
    """Gallery category response."""
    model_config = ConfigDict(from_attributes=True)

    uuid: str


class GalleryImagePage(BaseModel):
    items: list[GalleryImageRead]
    total: int
    page: int
    page_size: int


class GalleryCategoryPage(BaseModel):
    items: list[GalleryCategoryRead]
    total: int
    page: int
    page_size: int
