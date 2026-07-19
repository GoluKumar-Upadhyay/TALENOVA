"""Student testimonial records."""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class Testimonial(Base):
    """A moderated placement or learning testimonial."""
    __tablename__ = "testimonials"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True)
    student_name: Mapped[str] = mapped_column(String(180), index=True)
    college: Mapped[str | None] = mapped_column(String(255), nullable=True)
    designation: Mapped[str | None] = mapped_column(String(180), nullable=True)
    course_completed: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    review: Mapped[str] = mapped_column(Text)
    rating: Mapped[int] = mapped_column(Integer)
    photo_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    placement_company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    package: Mapped[str | None] = mapped_column(String(100), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
