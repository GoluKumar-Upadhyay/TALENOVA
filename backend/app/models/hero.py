from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class HeroSection(Base):
    __tablename__="hero_sections"
    id: Mapped[int]=mapped_column(primary_key=True)
    uuid: Mapped[str]=mapped_column(String(36),default=lambda:str(uuid4()),unique=True,index=True)
    heading: Mapped[str]=mapped_column(String(255))
    subheading: Mapped[str|None]=mapped_column(String(255),nullable=True)
    description: Mapped[str|None]=mapped_column(Text,nullable=True)
    button_text: Mapped[str|None]=mapped_column(String(80),nullable=True)
    button_link: Mapped[str|None]=mapped_column(String(500),nullable=True)
    hero_image_url: Mapped[str|None]=mapped_column(String(1000),nullable=True)
    background_image_url: Mapped[str|None]=mapped_column(String(1000),nullable=True)
    is_active: Mapped[bool]=mapped_column(Boolean,default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
class Statistic(Base):
    __tablename__="statistics"
    id: Mapped[int]=mapped_column(primary_key=True)
    uuid: Mapped[str]=mapped_column(String(36),default=lambda:str(uuid4()),unique=True,index=True)
    label: Mapped[str]=mapped_column(String(120))
    value: Mapped[int]=mapped_column(Integer)
    suffix: Mapped[str|None]=mapped_column(String(20),nullable=True)
    display_order: Mapped[int]=mapped_column(Integer,default=0)
    is_active: Mapped[bool]=mapped_column(Boolean,default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
