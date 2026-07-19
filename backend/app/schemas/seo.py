"""SEO API contracts."""
from pydantic import BaseModel, Field
class SEOWrite(BaseModel):
    page_key: str = Field(min_length=1, max_length=120)
    site_title: str | None = Field(default=None, max_length=255)
    meta_title: str = Field(min_length=1, max_length=255)
    meta_description: str | None = Field(default=None, max_length=1000)
    meta_keywords: list[str] = Field(default_factory=list)
    canonical_url: str | None = None
    robots_meta: str = "index,follow"
    open_graph: dict = Field(default_factory=dict)
    twitter_cards: dict = Field(default_factory=dict)
    hreflang: dict = Field(default_factory=dict)
    structured_data: dict = Field(default_factory=dict)
    sitemap_config: dict = Field(default_factory=dict)
    robots_txt: str | None = None
    verification_codes: dict = Field(default_factory=dict)
    redirect_rules: list[dict] = Field(default_factory=list)
    favicon_url: str | None = None
    is_active: bool = True
class SEORead(SEOWrite): uuid: str
class SEOPage(BaseModel):
    items: list[SEORead]
    total: int
    page: int
    page_size: int
