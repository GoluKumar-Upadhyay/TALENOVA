"""Success story API contracts."""
from pydantic import BaseModel, ConfigDict, Field


class SuccessStoryWrite(BaseModel):
    name: str = Field(min_length=2, max_length=180)
    image_url: str | None = Field(default=None, max_length=1000)
    course: str | None = Field(default=None, max_length=255)
    batch: str | None = Field(default=None, max_length=100)
    internship: str | None = Field(default=None, max_length=255)
    placement: str | None = Field(default=None, max_length=255)
    company_logo_url: str | None = Field(default=None, max_length=1000)
    job_role: str | None = Field(default=None, max_length=180)
    college: str | None = Field(default=None, max_length=255)
    graduation_year: int | None = Field(default=None, ge=1950, le=2100)
    before_journey: str | None = Field(default=None, max_length=20000)
    after_journey: str | None = Field(default=None, max_length=20000)
    linkedin_url: str | None = Field(default=None, max_length=1000)
    achievement_tags: list[str] = Field(default_factory=list)
    is_featured: bool = False
    salary: str | None = Field(default=None, max_length=100)
    story: str = Field(min_length=10, max_length=30000)
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True


class SuccessStoryRead(SuccessStoryWrite):
    model_config = ConfigDict(from_attributes=True)

    uuid: str


class SuccessStoryPage(BaseModel):
    items: list[SuccessStoryRead]
    total: int
    page: int
    page_size: int
