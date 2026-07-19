"""Global and page-specific SEO records."""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class SEORecord(Base):
    """SEO configuration for the global site or a named page."""
    __tablename__ = "seo_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True)
    page_key: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    site_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta_title: Mapped[str] = mapped_column(String(255))
    meta_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    meta_keywords: Mapped[list] = mapped_column(JSON, default=list)
    canonical_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    robots_meta: Mapped[str] = mapped_column(String(120), default="index,follow")
    open_graph: Mapped[dict] = mapped_column(JSON, default=dict)
    twitter_cards: Mapped[dict] = mapped_column(JSON, default=dict)
    hreflang: Mapped[dict] = mapped_column(JSON, default=dict)
    structured_data: Mapped[dict] = mapped_column(JSON, default=dict)
    sitemap_config: Mapped[dict] = mapped_column(JSON, default=dict)
    robots_txt: Mapped[str | None] = mapped_column(Text, nullable=True)
    verification_codes: Mapped[dict] = mapped_column(JSON, default=dict)
    redirect_rules: Mapped[list] = mapped_column(JSON, default=list)
    favicon_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
