"""Hierarchical navigation menu items."""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class NavigationItem(Base):
    """A visible internal or external navigation link."""
    __tablename__ = "navigation_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("navigation_items.id"), nullable=True)
    label: Mapped[str] = mapped_column(String(120))
    icon: Mapped[str | None] = mapped_column(String(80), nullable=True)
    href: Mapped[str] = mapped_column(String(1000))
    is_external: Mapped[bool] = mapped_column(Boolean, default=False)
    visible_roles: Mapped[list] = mapped_column(JSON, default=list)
    location: Mapped[str] = mapped_column(String(20), default="header")
    is_mega_menu: Mapped[bool] = mapped_column(Boolean, default=False)
    open_in_new_tab: Mapped[bool] = mapped_column(Boolean, default=False)
    authentication_required: Mapped[bool] = mapped_column(Boolean, default=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
