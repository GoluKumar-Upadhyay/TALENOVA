from __future__ import annotations

from sqlalchemy import func,select
from sqlalchemy.orm import Session
from app.models.course import Course
class CourseRepository:
 SORT_FIELDS={"title":Course.title,"display_order":Course.display_order,"created_at":Course.created_at,"duration":Course.duration}
 def __init__(self,db:Session):self.db=db
 def list(self,search,category_id,mentor_id,published,coming_soon,is_active,sort,direction,page,size):
  q=[Course.is_deleted.is_(False)]
  if search:q.append(Course.title.ilike(f"%{search}%"))
  if category_id is not None:q.append(Course.category_id==category_id)
  if mentor_id is not None:q.append(Course.mentor_id==mentor_id)
  if published is not None:q.append(Course.is_published==published)
  if coming_soon is not None:q.append(Course.is_coming_soon==coming_soon)
  if is_active is not None:q.append(Course.is_active==is_active)
  order=self.SORT_FIELDS[sort].desc() if direction=="desc" else self.SORT_FIELDS[sort].asc()
  return list(self.db.scalars(select(Course).where(*q).order_by(order).offset((page-1)*size).limit(size))),self.db.scalar(select(func.count()).select_from(Course).where(*q)) or 0
 def get(self,uuid):return self.db.scalar(select(Course).where(Course.uuid==uuid,Course.is_deleted.is_(False)))
 def create(self,data):item=Course(**data);self.db.add(item);self.db.commit();self.db.refresh(item);return item
 def save(self,item,data):
  for k,v in data.items():setattr(item,k,v)
  self.db.commit();self.db.refresh(item);return item
