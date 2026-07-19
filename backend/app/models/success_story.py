"""Student career success stories."""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class SuccessStory(Base):
    """A public outcome narrative for a TALENOVA student."""
    __tablename__ = "success_stories"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True)
    name: Mapped[str] = mapped_column(String(180), index=True)
    image_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    course: Mapped[str | None] = mapped_column(String(255), nullable=True)
    batch: Mapped[str | None] = mapped_column(String(100), nullable=True)
    internship: Mapped[str | None] = mapped_column(String(255), nullable=True)
    placement: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company_logo_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    job_role: Mapped[str | None] = mapped_column(String(180), nullable=True)
    college: Mapped[str | None] = mapped_column(String(255), nullable=True)
    graduation_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    before_journey: Mapped[str | None] = mapped_column(Text, nullable=True)
    after_journey: Mapped[str | None] = mapped_column(Text, nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    achievement_tags: Mapped[list] = mapped_column(JSON, default=list)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    salary: Mapped[str | None] = mapped_column(String(100), nullable=True)
    story: Mapped[str] = mapped_column(Text)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
