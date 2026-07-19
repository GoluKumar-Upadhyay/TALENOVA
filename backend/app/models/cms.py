from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class CmsItem(Base):
    __tablename__="cms_items"
    id: Mapped[int]=mapped_column(primary_key=True)
    uuid: Mapped[str]=mapped_column(String(36), default=lambda:str(uuid4()), unique=True, index=True)
    collection: Mapped[str]=mapped_column(String(80), index=True)
    slug: Mapped[str|None]=mapped_column(String(160), nullable=True, index=True)
    title: Mapped[str]=mapped_column(String(255))
    body: Mapped[str|None]=mapped_column(Text, nullable=True)
    data: Mapped[dict]=mapped_column(JSON, default=dict)
    display_order: Mapped[int]=mapped_column(Integer, default=0)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by: Mapped[int|None]=mapped_column(ForeignKey("users.id"), nullable=True)
    updated_by: Mapped[int|None]=mapped_column(ForeignKey("users.id"), nullable=True)
    is_active: Mapped[bool]=mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool]=mapped_column(Boolean, default=False)
