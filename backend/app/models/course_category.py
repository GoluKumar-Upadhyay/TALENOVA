from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean,DateTime,Integer,String,Text
from sqlalchemy.orm import Mapped,mapped_column
from app.db.base import Base
class CourseCategory(Base):
    __tablename__="course_categories"
    id:Mapped[int]=mapped_column(primary_key=True)
    uuid:Mapped[str]=mapped_column(String(36),default=lambda:str(uuid4()),unique=True,index=True)
    name:Mapped[str]=mapped_column(String(120),unique=True,index=True)
    slug:Mapped[str]=mapped_column(String(140),unique=True,index=True)
    description:Mapped[str|None]=mapped_column(Text,nullable=True)
    image_url:Mapped[str|None]=mapped_column(String(1000),nullable=True)
    display_order:Mapped[int]=mapped_column(Integer,default=0)
    is_active:Mapped[bool]=mapped_column(Boolean,default=True)
    is_deleted:Mapped[bool]=mapped_column(Boolean,default=False)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    updated_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
