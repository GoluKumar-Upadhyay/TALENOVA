from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class ManagedContent(Base):
    __tablename__="managed_content"
    id: Mapped[int]=mapped_column(primary_key=True)
    uuid: Mapped[str]=mapped_column(String(36),default=lambda:str(uuid4()),unique=True,index=True)
    module: Mapped[str]=mapped_column(String(80),index=True)
    title: Mapped[str]=mapped_column(String(255))
    slug: Mapped[str|None]=mapped_column(String(160),nullable=True,index=True)
    content: Mapped[str|None]=mapped_column(Text,nullable=True)
    fields: Mapped[dict]=mapped_column(JSON,default=dict)
    media_urls: Mapped[list]=mapped_column(JSON,default=list)
    display_order: Mapped[int]=mapped_column(Integer,default=0)
    is_active: Mapped[bool]=mapped_column(Boolean,default=True)
    is_deleted: Mapped[bool]=mapped_column(Boolean,default=False)
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
