"""Pydantic schemas for the full LMS Courses module."""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# ── Curriculum (legacy flat items) ───────────────────────────────────────────

class CurriculumItemWrite(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=10000)
    position: int = Field(default=0, ge=0)


class CurriculumItemRead(CurriculumItemWrite):
    model_config = ConfigDict(from_attributes=True)
    uuid: str


# ── Submodules ────────────────────────────────────────────────────────────────

class SubmoduleWrite(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=20000)
    position: int = Field(default=0, ge=0)


class SubmoduleRead(SubmoduleWrite):
    model_config = ConfigDict(from_attributes=True)
    uuid: str
    module_id: int


# ── Modules ───────────────────────────────────────────────────────────────────

class ModuleWrite(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=20000)
    position: int = Field(default=0, ge=0)
    submodules: list[SubmoduleWrite] = Field(default_factory=list)


class ModuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: str
    course_id: int
    title: str
    description: str | None = None
    position: int
    submodules: list[SubmoduleRead] = Field(default_factory=list)


class ModuleReorder(BaseModel):
    """Body for bulk-reorder of modules or submodules."""
    ordered_uuids: list[str]


# ── Batches ───────────────────────────────────────────────────────────────────

BatchStatus = Literal[
    "draft", "published", "upcoming", "active",
    "batch_full", "applications_closed", "expired", "hidden"
]
TimeSlot = Literal["morning", "afternoon", "evening", "weekend", "online", "offline", "hybrid"]


class BatchWrite(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    start_date: date | None = None
    end_date: date | None = None
    application_deadline: date | None = None
    max_seats: int | None = Field(default=None, ge=1)
    remaining_seats: int | None = Field(default=None, ge=0)
    time_slot: TimeSlot | None = None
    status: BatchStatus = "draft"


class BatchRead(BatchWrite):
    model_config = ConfigDict(from_attributes=True)
    uuid: str
    course_id: int


# ── Applications ──────────────────────────────────────────────────────────────

ApplicationStatus = Literal["pending", "approved", "rejected"]


class ApplicationWrite(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=30)
    college: str | None = Field(default=None, max_length=255)
    degree: str | None = Field(default=None, max_length=255)
    current_year: str | None = Field(default=None, max_length=50)
    linkedin_url: str | None = Field(default=None, max_length=1000)
    github_url: str | None = Field(default=None, max_length=1000)
    motivation: str | None = Field(default=None, max_length=5000)
    resume_url: str | None = Field(default=None, max_length=1000)
    batch_id: int | None = None


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus
    admin_notes: str | None = None


class ApplicationRead(ApplicationWrite):
    model_config = ConfigDict(from_attributes=True)
    uuid: str
    course_id: int
    status: ApplicationStatus
    admin_notes: str | None = None
    created_at: datetime


class ApplicationPage(BaseModel):
    items: list[ApplicationRead]
    total: int
    page: int
    page_size: int


# ── Course Create / Update ────────────────────────────────────────────────────

class CourseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    thumbnail_url: str | None = Field(default=None, max_length=1000)
    # All remaining fields optional
    slug: str | None = Field(default=None, max_length=180)
    category_id: int | None = Field(default=None, gt=0)
    mentor_id: int | None = Field(default=None, gt=0)
    short_description: str | None = Field(default=None, max_length=500)
    description: str | None = Field(default=None, max_length=50000)
    duration: str | None = Field(default=None, max_length=100)
    level: str | None = Field(default=None, max_length=50)
    price: float | None = Field(default=None, ge=0)
    certificate_available: bool = False
    skills_covered: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    learning_outcomes: list[str] = Field(default_factory=list)
    career_opportunities: list[str] = Field(default_factory=list)
    faqs: list[dict] = Field(default_factory=list)
    prerequisites: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    certification: str | None = Field(default=None, max_length=500)
    registration_url: str | None = Field(default=None, max_length=1000)
    is_coming_soon: bool = False
    is_published: bool = False
    display_order: int = Field(default=0, ge=0)
    curriculum: list[CurriculumItemWrite] = Field(default_factory=list)

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, value: str | None) -> str | None:
        if value is not None and not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", value):
            raise ValueError("slug may contain only lowercase letters, numbers, and hyphens")
        return value


class CourseUpdate(CourseCreate):
    title: str | None = Field(default=None, min_length=2, max_length=255)


class CourseStatusUpdate(BaseModel):
    is_active: bool | None = None
    is_published: bool | None = None
    is_coming_soon: bool | None = None


# ── Course Read ───────────────────────────────────────────────────────────────

class CourseRead(CourseCreate):
    model_config = ConfigDict(from_attributes=True)
    uuid: str
    is_active: bool
    is_published: bool
    is_deleted: bool
    curriculum: list[CurriculumItemRead] = Field(default_factory=list)
    modules: list[ModuleRead] = Field(default_factory=list)
    batches: list[BatchRead] = Field(default_factory=list)


class CourseCard(BaseModel):
    """Lightweight card for listing pages."""
    model_config = ConfigDict(from_attributes=True)
    uuid: str
    title: str
    slug: str
    short_description: str | None = None
    thumbnail_url: str | None = None
    level: str | None = None
    duration: str | None = None
    is_published: bool
    is_active: bool
    display_order: int
    category_id: int | None = None


class CoursePage(BaseModel):
    items: list[CourseRead]
    total: int
    page: int
    page_size: int


class CourseCardPage(BaseModel):
    items: list[CourseCard]
    total: int
    page: int
    page_size: int


# backward compat
CourseWrite = CourseCreate
