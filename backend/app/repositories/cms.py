from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.cms import CmsItem
class CmsRepository:
    def __init__(self,db:Session): self.db=db
    def list(self,collection:str,page:int,size:int):
        where=(CmsItem.collection==collection,CmsItem.is_deleted.is_(False),CmsItem.is_active.is_(True))
        return list(self.db.scalars(select(CmsItem).where(*where).order_by(CmsItem.display_order).offset((page-1)*size).limit(size))),self.db.scalar(select(func.count()).select_from(CmsItem).where(*where)) or 0
    def create(self,collection:str,values:dict,user_id:int|None):
        item=CmsItem(collection=collection,created_by=user_id,updated_by=user_id,**values); self.db.add(item);self.db.commit();self.db.refresh(item);return item
    def get(self,uuid:str): return self.db.scalar(select(CmsItem).where(CmsItem.uuid==uuid,CmsItem.is_deleted.is_(False)))
    def update(self,item:CmsItem,values:dict,user_id:int|None):
        for key,value in values.items():setattr(item,key,value)
        item.updated_by=user_id;self.db.commit();self.db.refresh(item);return item
    def delete(self,item:CmsItem,user_id:int|None): item.is_deleted=True;item.updated_by=user_id;self.db.commit()
