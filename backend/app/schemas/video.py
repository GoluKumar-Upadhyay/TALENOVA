"""Video API contracts with automatic provider detection."""

import re
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


# Patterns for URL-based provider detection
_YOUTUBE = re.compile(
    r"(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)[\w\-]+"
)
_DRIVE = re.compile(
    r"(?:https?://)?(?:drive\.google\.com|docs\.google\.com)/(?:file/d/|open\?id=)[\w\-]+"
)
_VIMEO = re.compile(r"(?:https?://)?(?:www\.)?vimeo\.com/\d+")


VideoType = Literal["youtube", "drive", "vimeo", "upload"]


def _detect_type(youtube_url: str | None, video_url: str | None) -> VideoType | None:
    """Derive the provider from the stored URL fields."""
    if youtube_url:
        if _YOUTUBE.search(youtube_url):
            return "youtube"
        if _VIMEO.search(youtube_url):
            return "vimeo"
        if _DRIVE.search(youtube_url):
            return "drive"
        # Unknown external URL — still accept but type stays None (handled below)
        return "youtube"  # default: treat any url in youtube_url field as youtube
    if video_url:
        return "upload"
    return None


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
            raise ValueError("A YouTube URL, Google Drive URL, Vimeo URL, or uploaded video URL is required")

        # Validate youtube_url patterns when provided
        if self.youtube_url:
            url = self.youtube_url.strip()
            is_youtube = bool(_YOUTUBE.search(url))
            is_vimeo   = bool(_VIMEO.search(url))
            is_drive   = bool(_DRIVE.search(url))
            # Must match at least one supported provider OR be a bare https URL
            if not (is_youtube or is_vimeo or is_drive or url.startswith("https://")):
                raise ValueError(
                    "youtube_url must be a YouTube (youtu.be / youtube.com), "
                    "Vimeo (vimeo.com), Google Drive, or HTTPS URL"
                )

        # Validate video_url must be HTTPS (Supabase upload)
        if self.video_url and not self.video_url.startswith("https://"):
            raise ValueError("video_url must use HTTPS")

        return self


class VideoRead(VideoWrite):
    model_config = ConfigDict(from_attributes=True)

    uuid: str
    video_type: VideoType | None = None

    @model_validator(mode="after")
    def compute_video_type(self):
        """Compute video_type from URL fields so the frontend knows how to render."""
        self.video_type = _detect_type(self.youtube_url, self.video_url)
        return self


class VideoPage(BaseModel):
    items: list[VideoRead]
    total: int
    page: int
    page_size: int
