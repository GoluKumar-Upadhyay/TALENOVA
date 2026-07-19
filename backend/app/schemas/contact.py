"""Contact inquiry contracts."""
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContactWrite(BaseModel):
    contact_type: str = Field(pattern="^(student|college|industry)$")
    name: str = Field(min_length=2, max_length=180)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=40)
    organization: str | None = Field(default=None, max_length=255)
    designation: str | None = Field(default=None, max_length=180)
    website: str | None = Field(default=None, max_length=1000)
    course_interested: str | None = Field(default=None, max_length=255)
    training_requirements: str | None = Field(default=None, max_length=10000)
    expected_students: int | None = Field(default=None, ge=1)
    preferred_dates: str | None = Field(default=None, max_length=255)
    subject: str = Field(min_length=2, max_length=255)
    message: str = Field(min_length=10, max_length=20000)


class ContactRead(ContactWrite):
    model_config = ConfigDict(from_attributes=True)

    uuid: str
    status: str
    is_read: bool
    is_archived: bool


class ContactPage(BaseModel):
    items: list[ContactRead]
    total: int
    page: int
    page_size: int
