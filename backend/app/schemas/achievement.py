"""Achievement API contracts."""
from pydantic import BaseModel, Field
class AchievementWrite(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str | None = Field(default=None, max_length=10000)
    image_url: str | None = Field(default=None, max_length=1000)
    achievement_type: str = Field(default="recognition", min_length=2, max_length=100)
    is_featured: bool = False
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True
class AchievementRead(AchievementWrite): uuid: str
class AchievementPage(BaseModel):
    items: list[AchievementRead]
    total: int
    page: int
    page_size: int
