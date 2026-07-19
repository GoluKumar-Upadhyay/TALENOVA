from pydantic import BaseModel, Field, HttpUrl
class HeroWrite(BaseModel):
    heading:str=Field(min_length=1,max_length=255);subheading:str|None=None;description:str|None=None;button_text:str|None=None;button_link:str|None=None;hero_image_url:str|None=None;background_image_url:str|None=None;is_active:bool=True
class HeroRead(HeroWrite): uuid:str
class StatisticWrite(BaseModel): label:str=Field(min_length=1,max_length=120);value:int=Field(ge=0);suffix:str|None=None;display_order:int=0;is_active:bool=True
class StatisticRead(StatisticWrite): uuid:str
class HeroPage(BaseModel): items:list[HeroRead];total:int;page:int;page_size:int
class StatisticPage(BaseModel): items:list[StatisticRead];total:int;page:int;page_size:int
