"""Editable footer configuration."""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class FooterConfiguration(Base):
    """Singleton footer content document."""
    __tablename__ = "footer_configurations"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True)
    logo_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sections: Mapped[list] = mapped_column(JSON, default=list)
    quick_links: Mapped[list] = mapped_column(JSON, default=list)
    contact_details: Mapped[dict] = mapped_column(JSON, default=dict)
    social_links: Mapped[dict] = mapped_column(JSON, default=dict)
    copyright_text: Mapped[str | None] = mapped_column(String(500), nullable=True)
    newsletter_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    newsletter_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    legal_links: Mapped[list] = mapped_column(JSON, default=list)
    display_order: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
