"""Project API contracts."""
from pydantic import BaseModel, Field
class ProjectWrite(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str | None = Field(default=None, max_length=20000)
    image_url: str | None = Field(default=None, max_length=1000)
    github_url: str | None = Field(default=None, max_length=1000)
    demo_url: str | None = Field(default=None, max_length=1000)
    technologies: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    screenshot_urls: list[str] = Field(default_factory=list)
    status: str = Field(default="ongoing", pattern="^(completed|ongoing|archived)$")
    is_featured: bool = False
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True
class ProjectRead(ProjectWrite): uuid: str
class ProjectPage(BaseModel):
    items: list[ProjectRead]
    total: int
    page: int
    page_size: int
