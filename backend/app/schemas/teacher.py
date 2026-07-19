"""Teacher API validation and representation contracts."""

from pydantic import BaseModel, EmailStr, Field


class TeacherWrite(BaseModel):
    """Validated teacher data accepted from CMS administrators."""

    name: str = Field(min_length=2, max_length=180)
    designation: str = Field(min_length=2, max_length=180)
    biography: str | None = Field(default=None, max_length=20000)
    qualification: str | None = Field(default=None, max_length=500)
    experience: str | None = Field(default=None, max_length=500)
    image_url: str | None = Field(default=None, max_length=1000)
    email: EmailStr | None = None
    linkedin_url: str | None = Field(default=None, max_length=1000)
    github_url: str | None = Field(default=None, max_length=1000)
    skills: list[str] = Field(default_factory=list)
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True


class TeacherRead(TeacherWrite):
    """Public teacher payload returned by API collection endpoints."""

    uuid: str


class TeacherPage(BaseModel):
    """Paginated teacher list response."""

    items: list[TeacherRead]
    total: int
    page: int
    page_size: int
