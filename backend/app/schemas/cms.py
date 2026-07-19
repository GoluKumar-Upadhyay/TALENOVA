from pydantic import BaseModel, Field
class ItemWrite(BaseModel):
    title: str=Field(min_length=1,max_length=255)
    slug: str|None=None
    body: str|None=None
    data: dict=Field(default_factory=dict)
    display_order: int=0
    is_active: bool=True
class ItemRead(ItemWrite):
    uuid: str
class Page(BaseModel):
    items: list[ItemRead]
    total: int
    page: int
    page_size: int
