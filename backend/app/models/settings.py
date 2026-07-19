"""Editable website settings."""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class WebsiteSettings(Base):
    """Singleton settings document for the public website."""
    __tablename__ = "website_settings"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True)
    site_name: Mapped[str] = mapped_column(String(255))
    tagline: Mapped[str | None] = mapped_column(String(255), nullable=True)
    default_language: Mapped[str] = mapped_column(String(20), default="en")
    timezone: Mapped[str] = mapped_column(String(80), default="UTC")
    site_logo_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    favicon_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    hero_defaults: Mapped[dict] = mapped_column(JSON, default=dict)
    contact_information: Mapped[dict] = mapped_column(JSON, default=dict)
    social_links: Mapped[dict] = mapped_column(JSON, default=dict)
    email_settings: Mapped[dict] = mapped_column(JSON, default=dict)
    theme_settings: Mapped[dict] = mapped_column(JSON, default=dict)
    homepage_configuration: Mapped[dict] = mapped_column(JSON, default=dict)
    analytics_keys: Mapped[dict] = mapped_column(JSON, default=dict)
    seo_defaults: Mapped[dict] = mapped_column(JSON, default=dict)
    maintenance_message: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    default_theme: Mapped[str] = mapped_column(String(30), default="light")
    pagination_size: Mapped[int] = mapped_column(default=24)
    maintenance_mode: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
