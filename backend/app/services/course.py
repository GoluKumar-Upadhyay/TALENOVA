from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.course import CourseRepository
class CourseService:
 SORT_FIELDS=set(CourseRepository.SORT_FIELDS)
 def __init__(self,db:Session):self.repo=CourseRepository(db)
 def list(self,*args):
  sort=args[6];direction=args[7]
  if sort not in self.SORT_FIELDS:raise HTTPException(422,"Unsupported course sort field")
  if direction not in {"asc","desc"}:raise HTTPException(422,"Unsupported sort direction")
  return self.repo.list(*args)
 def get(self,uuid):
  item=self.repo.get(uuid)
  if not item:raise HTTPException(404,"Course not found")
  return item
 def create(self,data):return self.repo.create(data)
 def update(self,uuid,data):
  item=self.get(uuid)
  return self.repo.save(item,data)
 def delete(self,uuid):
  item=self.get(uuid)
  self.repo.save(item,{"is_deleted":True})
