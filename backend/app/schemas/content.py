from pydantic import BaseModel,Field
class ContentWrite(BaseModel):
    title:str=Field(min_length=1,max_length=255)
    slug:str|None=None
    content:str|None=None
    fields:dict=Field(default_factory=dict)
    media_urls:list[str]=Field(default_factory=list)
    display_order:int=0
    is_active:bool=True
class ContentRead(ContentWrite):uuid:str
class ResultPage(BaseModel):items:list[ContentRead];total:int;page:int;page_size:int
