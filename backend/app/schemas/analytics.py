"""Dashboard analytics response contracts."""
from datetime import date
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class DateRange(BaseModel):
    start: date | None = None
    end: date | None = None


class DashboardSummary(BaseModel):
    total_courses: int
    total_students: int
    total_teachers: int
    total_contacts: int
    total_events: int
    total_internships: int
    total_testimonials: int
    total_success_stories: int
    total_gallery_images: int
    total_videos: int


class AnalyticsResponse(BaseModel):
    summary: DashboardSummary
    monthly_contacts: list[dict]
    monthly_events: list[dict]
    monthly_internships: list[dict]
    recent_activities: list[dict]


class AnalyticsEventWrite(BaseModel):
    event_type: str = Field(min_length=2, max_length=80)
    occurred_at: datetime | None = None
    event_metadata: dict = Field(default_factory=dict)


class AnalyticsEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: str
    event_type: str
    occurred_at: datetime
    event_metadata: dict


class AnalyticsEventPage(BaseModel):
    items: list[AnalyticsEventRead]
    total: int
    page: int
    page_size: int
