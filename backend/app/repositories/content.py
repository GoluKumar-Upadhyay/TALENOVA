from __future__ import annotations

from sqlalchemy import func,select
from sqlalchemy.orm import Session
from app.models.content import ManagedContent
class ContentRepository:
    SORT_FIELDS={"title":ManagedContent.title,"display_order":ManagedContent.display_order,"created_at":ManagedContent.created_at,"updated_at":ManagedContent.updated_at}
    def __init__(self,db:Session):self.db=db
    def list(self,module,search,is_active,sort,direction,page,size):
        q=(ManagedContent.module==module,ManagedContent.is_deleted.is_(False))
        filters=list(q)
        if search:filters.append(ManagedContent.title.ilike(f"%{search}%"))
        if is_active is not None:filters.append(ManagedContent.is_active==is_active)
        order=self.SORT_FIELDS[sort].desc() if direction=="desc" else self.SORT_FIELDS[sort].asc()
        return list(self.db.scalars(select(ManagedContent).where(*filters).order_by(order).offset((page-1)*size).limit(size))),self.db.scalar(select(func.count()).select_from(ManagedContent).where(*filters)) or 0
    def get(self,uuid):return self.db.scalar(select(ManagedContent).where(ManagedContent.uuid==uuid,ManagedContent.is_deleted.is_(False)))
    def create(self,module,data):item=ManagedContent(module=module,**data);self.db.add(item);self.db.commit();self.db.refresh(item);return item
    def save(self,item,data):
        for key,value in data.items():setattr(item,key,value)
        self.db.commit();self.db.refresh(item);return item
