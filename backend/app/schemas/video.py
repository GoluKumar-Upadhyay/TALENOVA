"""Video API contracts."""
from pydantic import BaseModel, Field, model_validator
class VideoWrite(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str | None = Field(default=None, max_length=20000)
    category: str = Field(min_length=2, max_length=120)
    youtube_url: str | None = Field(default=None, max_length=1000)
    video_url: str | None = Field(default=None, max_length=1000)
    thumbnail_url: str | None = Field(default=None, max_length=1000)
    duration_seconds: int | None = Field(default=None, ge=0)
    is_featured: bool = False
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True
    @model_validator(mode="after")
    def require_video_source(self):
        if not self.youtube_url and not self.video_url:
            raise ValueError("A YouTube URL or uploaded video URL is required")
        return self
class VideoRead(VideoWrite): uuid: str
class VideoPage(BaseModel):
    items: list[VideoRead]
    total: int
    page: int
    page_size: int
