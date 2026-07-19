"""Website settings contracts."""
from pydantic import BaseModel, ConfigDict, Field


class SettingsWrite(BaseModel):
    site_name: str = Field(min_length=2, max_length=255)
    tagline: str | None = Field(default=None, max_length=255)
    default_language: str = Field(default="en", min_length=2, max_length=20)
    timezone: str = Field(default="UTC", min_length=2, max_length=80)
    site_logo_url: str | None = None
    favicon_url: str | None = None
    hero_defaults: dict = Field(default_factory=dict)
    contact_information: dict = Field(default_factory=dict)
    social_links: dict = Field(default_factory=dict)
    email_settings: dict = Field(default_factory=dict)
    theme_settings: dict = Field(default_factory=dict)
    homepage_configuration: dict = Field(default_factory=dict)
    analytics_keys: dict = Field(default_factory=dict)
    seo_defaults: dict = Field(default_factory=dict)
    maintenance_mode: bool = False
    maintenance_message: str | None = Field(default=None, max_length=1000)
    default_theme: str = Field(default="light", pattern="^(light)$")
    pagination_size: int = Field(default=24, ge=1, le=100)


class SettingsRead(SettingsWrite):
    model_config = ConfigDict(from_attributes=True)

    uuid: str


class SettingsPage(BaseModel):
    items: list[SettingsRead]
    total: int
    page: int
    page_size: int
