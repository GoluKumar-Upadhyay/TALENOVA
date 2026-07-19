"""Persistent course entities and their normalized curriculum records."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

PortableJSONB = JSON().with_variant(JSONB, "postgresql")


class Course(Base):
    """A publishable TALENOVA programme managed by administrators."""

    __tablename__ = "courses"
    __table_args__ = (
        Index("ix_courses_active_order", "is_deleted", "is_active", "display_order"),
        Index("ix_courses_category_status", "category_id", "is_deleted", "is_active"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(
        String(36), default=lambda: str(uuid4()), unique=True, index=True
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("course_categories.id", ondelete="SET NULL"), nullable=True
    )
    mentor_id: Mapped[int | None] = mapped_column(
        ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), index=True)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    short_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    duration: Mapped[str | None] = mapped_column(String(100), nullable=True)
    prerequisites: Mapped[list] = mapped_column(PortableJSONB, default=list)
    tools: Mapped[list] = mapped_column(PortableJSONB, default=list)
    projects: Mapped[list] = mapped_column(PortableJSONB, default=list)
    certification: Mapped[str | None] = mapped_column(String(500), nullable=True)
    registration_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_coming_soon: Mapped[bool] = mapped_column(Boolean, default=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    curriculum: Mapped[list["CourseCurriculumItem"]] = relationship(
        back_populates="course", cascade="all, delete-orphan", order_by="CourseCurriculumItem.position"
    )


class CourseCurriculumItem(Base):
    """An ordered unit in a course curriculum."""

    __tablename__ = "course_curriculum_items"
    __table_args__ = (Index("ix_curriculum_course_position", "course_id", "position"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(
        String(36), default=lambda: str(uuid4()), unique=True, index=True
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    position: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    course: Mapped[Course] = relationship(back_populates="curriculum")
