from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.course_category import CourseCategoryRepository
class CourseCategoryService:
    def __init__(self,db:Session):self.repo=CourseCategoryRepository(db)
    def list(self,*args):return self.repo.list(*args)
    def create(self,data):return self.repo.create(data)
    def update(self,uuid,data):
        item=self.repo.get(uuid)
        if not item:raise HTTPException(404,"Course category not found")
        return self.repo.save(item,data)
    def delete(self,uuid):
        item=self.repo.get(uuid)
        if not item:raise HTTPException(404,"Course category not found")
        self.repo.save(item,{"is_deleted":True})
