"""Testimonial API contracts."""
from pydantic import BaseModel, Field
class TestimonialWrite(BaseModel):
    student_name: str = Field(min_length=2, max_length=180)
    college: str | None = Field(default=None, max_length=255)
    designation: str | None = Field(default=None, max_length=180)
    course_completed: str | None = Field(default=None, max_length=255)
    review: str = Field(min_length=5, max_length=10000)
    rating: int = Field(ge=1, le=5)
    photo_url: str | None = Field(default=None, max_length=1000)
    placement_company: str | None = Field(default=None, max_length=255)
    package: str | None = Field(default=None, max_length=100)
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True
    is_featured: bool = False
class TestimonialRead(TestimonialWrite): uuid: str
class TestimonialPage(BaseModel):
    items: list[TestimonialRead]
    total: int
    page: int
    page_size: int
