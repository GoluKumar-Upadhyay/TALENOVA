"""Workshop event contracts."""
from pydantic import BaseModel, Field
class EventWrite(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str | None = Field(default=None, max_length=20000)
    event_type: str = Field(default="workshop", min_length=2, max_length=80)
    start_date: str | None = Field(default=None, max_length=40)
    end_date: str | None = Field(default=None, max_length=40)
    registration_deadline: str | None = Field(default=None, max_length=40)
    event_date: str | None = Field(default=None, max_length=40)
    location: str | None = Field(default=None, max_length=255)
    google_maps_url: str | None = Field(default=None, max_length=1000)
    mode: str = Field(default="online", pattern="^(online|offline|hybrid)$")
    registration_url: str | None = Field(default=None, max_length=1000)
    banner_url: str | None = Field(default=None, max_length=1000)
    gallery_urls: list[str] = Field(default_factory=list)
    speaker_details: dict = Field(default_factory=dict)
    maximum_participants: int | None = Field(default=None, ge=1)
    is_featured: bool = False
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True
class EventRead(EventWrite): uuid: str
class EventPage(BaseModel):
    items: list[EventRead]
    total: int
    page: int
    page_size: int
