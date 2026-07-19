"""Pydantic request, filter, and response contracts for courses."""

from pydantic import BaseModel, Field, HttpUrl, field_validator


class CurriculumItemWrite(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=10000)
    position: int = Field(default=0, ge=0)


class CurriculumItemRead(CurriculumItemWrite):
    uuid: str


class CourseCreate(BaseModel):
    category_id: int | None = Field(default=None, gt=0)
    mentor_id: int | None = Field(default=None, gt=0)
    title: str = Field(min_length=2, max_length=255)
    slug: str | None = Field(default=None, max_length=180)
    short_description: str | None = Field(default=None, max_length=500)
    description: str | None = Field(default=None, max_length=50000)
    thumbnail_url: str | None = Field(default=None, max_length=1000)
    duration: str | None = Field(default=None, max_length=100)
    prerequisites: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    certification: str | None = Field(default=None, max_length=500)
    registration_url: str | None = Field(default=None, max_length=1000)
    is_coming_soon: bool = False
    display_order: int = Field(default=0, ge=0)
    curriculum: list[CurriculumItemWrite] = Field(default_factory=list)

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, value: str | None) -> str | None:
        if value is not None and not value.replace("-", "").isalnum():
            raise ValueError("slug may contain only letters, numbers, and hyphens")
        return value


class CourseUpdate(CourseCreate):
    title: str | None = Field(default=None, min_length=2, max_length=255)


class CourseStatusUpdate(BaseModel):
    is_active: bool | None = None
    is_published: bool | None = None
    is_coming_soon: bool | None = None


class CourseRead(CourseCreate):
    uuid: str
    is_active: bool
    is_published: bool
    is_deleted: bool


class CoursePage(BaseModel):
    items: list[CourseRead]
    total: int
    page: int
    page_size: int


# Backward-compatible alias used by the existing router while it is upgraded.
CourseWrite = CourseCreate
