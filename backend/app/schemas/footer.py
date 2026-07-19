"""Footer API contracts."""
from pydantic import BaseModel, Field
class FooterWrite(BaseModel):
    logo_url: str | None = None
    description: str | None = Field(default=None, max_length=10000)
    sections: list[dict] = Field(default_factory=list)
    quick_links: list[dict] = Field(default_factory=list)
    contact_details: dict = Field(default_factory=dict)
    social_links: dict = Field(default_factory=dict)
    copyright_text: str | None = Field(default=None, max_length=500)
    newsletter_enabled: bool = False
    newsletter_label: str | None = Field(default=None, max_length=255)
    legal_links: list[dict] = Field(default_factory=list)
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True
class FooterRead(FooterWrite): uuid: str
class FooterPage(BaseModel):
    items: list[FooterRead]
    total: int
    page: int
    page_size: int
