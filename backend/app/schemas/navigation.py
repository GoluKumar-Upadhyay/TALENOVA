"""Navigation API contracts."""
from pydantic import BaseModel, ConfigDict, Field


class NavigationWrite(BaseModel):
    parent_id: int | None = None
    label: str = Field(min_length=1, max_length=120)
    icon: str | None = None
    href: str = Field(min_length=1, max_length=1000)
    is_external: bool = False
    location: str = Field(default="header", pattern="^(header|footer|mobile)$")
    is_mega_menu: bool = False
    open_in_new_tab: bool = False
    authentication_required: bool = False
    visible_roles: list[str] = Field(default_factory=list)
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True


class NavigationRead(NavigationWrite):
    model_config = ConfigDict(from_attributes=True)

    uuid: str


class NavigationPage(BaseModel):
    items: list[NavigationRead]
    total: int
    page: int
    page_size: int
