from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.content import ContentRepository
class ContentService:
    SORT_FIELDS=set(ContentRepository.SORT_FIELDS)
    def __init__(self,db:Session):self.repo=ContentRepository(db)
    def list(self,module,search,is_active,sort,direction,page,page_size):
        if sort not in self.SORT_FIELDS:raise HTTPException(422,"Unsupported content sort field")
        if direction not in {"asc","desc"}:raise HTTPException(422,"Unsupported sort direction")
        return self.repo.list(module,search,is_active,sort,direction,page,page_size)
    def get(self,uuid):
        item=self.repo.get(uuid)
        if not item:raise HTTPException(404,"Content not found")
        return item
    def create(self,module,data):return self.repo.create(module,data)
    def update(self,uuid,data):
        item=self.get(uuid)
        return self.repo.save(item,data)
    def delete(self,uuid):
        item=self.get(uuid)
        item.is_deleted=True;self.repo.save(item,{})
