"""FAQ API contracts."""
from pydantic import BaseModel, Field
class FAQWrite(BaseModel):
    question: str = Field(min_length=5, max_length=500)
    answer: str = Field(min_length=1, max_length=30000)
    page: str = Field(default="general", min_length=2, max_length=80)
    category: str = Field(default="general", pattern="^(admissions|courses|internships|placements|payments|general)$")
    seo_slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    is_featured: bool = False
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True
class FAQRead(FAQWrite): uuid: str
class FAQEngagement(BaseModel): helpful: bool
class FAQPage(BaseModel):
    items: list[FAQRead]
    total: int
    page: int
    page_size: int
