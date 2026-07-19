"""Internship API contracts."""
from pydantic import BaseModel, Field
class InternshipWrite(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str | None = Field(default=None, max_length=20000)
    company: str | None = Field(default=None, max_length=255)
    company_logo_url: str | None = Field(default=None, max_length=1000)
    internship_type: str = Field(default="online", pattern="^(online|offline|hybrid)$")
    duration: str | None = Field(default=None, max_length=100)
    stipend: str | None = Field(default=None, max_length=100)
    location: str | None = Field(default=None, max_length=255)
    eligibility: str | None = Field(default=None, max_length=10000)
    application_url: str | None = Field(default=None, max_length=1000)
    last_date: str | None = Field(default=None, max_length=40)
    skills: list[str] = Field(default_factory=list)
    is_coming_soon: bool = False
    is_featured: bool = False
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True
class InternshipRead(InternshipWrite): uuid: str
class InternshipPage(BaseModel):
    items: list[InternshipRead]
    total: int
    page: int
    page_size: int
