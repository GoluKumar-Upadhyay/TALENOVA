"""
Full LMS course models: Course + CourseModule + CourseSubmodule + CourseBatch + CourseApplication.
Existing CourseCurriculumItem is kept for backward compatibility.
"""

from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Index, Integer, JSON, Numeric, String, Text
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
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("course_categories.id", ondelete="SET NULL"), nullable=True)
    mentor_id: Mapped[int | None] = mapped_column(ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    short_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    duration: Mapped[str | None] = mapped_column(String(100), nullable=True)
    level: Mapped[str | None] = mapped_column(String(50), nullable=True)   # Beginner / Intermediate / Advanced
    price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    certificate_available: Mapped[bool] = mapped_column(Boolean, default=False)
    skills_covered: Mapped[list] = mapped_column(PortableJSONB, default=list)
    technologies: Mapped[list] = mapped_column(PortableJSONB, default=list)
    learning_outcomes: Mapped[list] = mapped_column(PortableJSONB, default=list)
    career_opportunities: Mapped[list] = mapped_column(PortableJSONB, default=list)
    faqs: Mapped[list] = mapped_column(PortableJSONB, default=list)         # [{question, answer}]
    prerequisites: Mapped[list] = mapped_column(PortableJSONB, default=list)
    tools: Mapped[list] = mapped_column(PortableJSONB, default=list)
    projects: Mapped[list] = mapped_column(PortableJSONB, default=list)
    certification: Mapped[str | None] = mapped_column(String(500), nullable=True)
    registration_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_coming_soon: Mapped[bool] = mapped_column(Boolean, default=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    curriculum: Mapped[list["CourseCurriculumItem"]] = relationship(
        back_populates="course", cascade="all, delete-orphan",
        order_by="CourseCurriculumItem.position",
    )
    modules: Mapped[list["CourseModule"]] = relationship(
        back_populates="course", cascade="all, delete-orphan",
        order_by="CourseModule.position",
    )
    batches: Mapped[list["CourseBatch"]] = relationship(
        back_populates="course", cascade="all, delete-orphan",
        order_by="CourseBatch.start_date",
    )
    applications: Mapped[list["CourseApplication"]] = relationship(
        back_populates="course", cascade="all, delete-orphan",
    )


class CourseCurriculumItem(Base):
    """Legacy flat curriculum item — kept for backward compatibility."""

    __tablename__ = "course_curriculum_items"
    __table_args__ = (Index("ix_curriculum_course_position", "course_id", "position"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    position: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    course: Mapped[Course] = relationship(back_populates="curriculum")


class CourseModule(Base):
    """A top-level module in a course curriculum."""

    __tablename__ = "course_modules"
    __table_args__ = (Index("ix_course_modules_course_pos", "course_id", "position"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    position: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    course: Mapped[Course] = relationship(back_populates="modules")
    submodules: Mapped[list["CourseSubmodule"]] = relationship(
        back_populates="module", cascade="all, delete-orphan",
        order_by="CourseSubmodule.position",
    )


class CourseSubmodule(Base):
    """A child topic inside a CourseModule."""

    __tablename__ = "course_submodules"
    __table_args__ = (Index("ix_course_submodules_mod_pos", "module_id", "position"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("course_modules.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    position: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    module: Mapped[CourseModule] = relationship(back_populates="submodules")


BATCH_STATUSES = ("draft", "published", "upcoming", "active", "batch_full", "applications_closed", "expired", "hidden")
TIME_SLOTS = ("morning", "afternoon", "evening", "weekend", "online", "offline", "hybrid")


class CourseBatch(Base):
    """A scheduled run of a course."""

    __tablename__ = "course_batches"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    application_deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    max_seats: Mapped[int | None] = mapped_column(Integer, nullable=True)
    remaining_seats: Mapped[int | None] = mapped_column(Integer, nullable=True)
    time_slot: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    course: Mapped[Course] = relationship(back_populates="batches")
    applications: Mapped[list["CourseApplication"]] = relationship(back_populates="batch")


APPLICATION_STATUSES = ("pending", "approved", "rejected")


class CourseApplication(Base):
    """A student application for a course."""

    __tablename__ = "course_applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    batch_id: Mapped[int | None] = mapped_column(ForeignKey("course_batches.id", ondelete="SET NULL"), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), index=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    college: Mapped[str | None] = mapped_column(String(255), nullable=True)
    degree: Mapped[str | None] = mapped_column(String(255), nullable=True)
    current_year: Mapped[str | None] = mapped_column(String(50), nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    github_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    motivation: Mapped[str | None] = mapped_column(Text, nullable=True)
    resume_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="pending")
    admin_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    course: Mapped[Course] = relationship(back_populates="applications")
    batch: Mapped[CourseBatch | None] = relationship(back_populates="applications")
