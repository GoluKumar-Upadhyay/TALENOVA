from sqlalchemy import func,select
from sqlalchemy.orm import Session
from app.models.course_category import CourseCategory
class CourseCategoryRepository:
    def __init__(self,db:Session):self.db=db
    def list(self,search,page,size):
        q=[CourseCategory.is_deleted.is_(False)]
        if search:q.append(CourseCategory.name.ilike(f"%{search}%"))
        return list(self.db.scalars(select(CourseCategory).where(*q).order_by(CourseCategory.display_order).offset((page-1)*size).limit(size))),self.db.scalar(select(func.count()).select_from(CourseCategory).where(*q)) or 0
    def get(self,uuid):return self.db.scalar(select(CourseCategory).where(CourseCategory.uuid==uuid,CourseCategory.is_deleted.is_(False)))
    def create(self,data):item=CourseCategory(**data);self.db.add(item);self.db.commit();self.db.refresh(item);return item
    def save(self,item,data):
        for key,value in data.items():setattr(item,key,value)
        self.db.commit();self.db.refresh(item);return item
