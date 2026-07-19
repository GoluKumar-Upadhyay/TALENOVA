"""Internship programme records."""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class InternshipProgram(Base):
    """An editable internship opportunity or programme."""
    __tablename__ = "internship_programs"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company_logo_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    internship_type: Mapped[str] = mapped_column(String(20), default="online")
    duration: Mapped[str | None] = mapped_column(String(100), nullable=True)
    stipend: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    eligibility: Mapped[str | None] = mapped_column(Text, nullable=True)
    application_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    last_date: Mapped[str | None] = mapped_column(String(40), nullable=True)
    skills: Mapped[list] = mapped_column(JSON, default=list)
    is_coming_soon: Mapped[bool] = mapped_column(Boolean, default=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
