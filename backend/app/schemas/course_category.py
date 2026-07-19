from pydantic import BaseModel,Field
class CourseCategoryWrite(BaseModel):
    name:str=Field(min_length=2,max_length=120);slug:str=Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$");description:str|None=None;image_url:str|None=None;display_order:int=0;is_active:bool=True
class CourseCategoryRead(CourseCategoryWrite):uuid:str
class CategoryPage(BaseModel):items:list[CourseCategoryRead];total:int;page:int;page_size:int
