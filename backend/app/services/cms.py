from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.cms import CmsRepository
class CmsService:
    def __init__(self,db:Session):self.repo=CmsRepository(db)
    def list(self,collection,page,size):return self.repo.list(collection,page,size)
    def create(self,collection,data,user_id):return self.repo.create(collection,data,user_id)
    def update(self,uuid,data,user_id):
        item=self.repo.get(uuid)
        if not item:raise HTTPException(404,"Content not found")
        return self.repo.update(item,data,user_id)
    def delete(self,uuid,user_id):
        item=self.repo.get(uuid)
        if not item:raise HTTPException(404,"Content not found")
        self.repo.delete(item,user_id)
