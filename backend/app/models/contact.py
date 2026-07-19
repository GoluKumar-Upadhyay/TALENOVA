"""Student and college contact inquiries."""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class ContactMessage(Base):
    """A contact inquiry submitted by a student or institution."""
    __tablename__ = "contact_messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True)
    contact_type: Mapped[str] = mapped_column(String(20), index=True)
    name: Mapped[str] = mapped_column(String(180))
    email: Mapped[str] = mapped_column(String(255), index=True)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    organization: Mapped[str | None] = mapped_column(String(255), nullable=True)
    designation: Mapped[str | None] = mapped_column(String(180), nullable=True)
    website: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    course_interested: Mapped[str | None] = mapped_column(String(255), nullable=True)
    training_requirements: Mapped[str | None] = mapped_column(Text, nullable=True)
    expected_students: Mapped[int | None] = mapped_column(Integer, nullable=True)
    preferred_dates: Mapped[str | None] = mapped_column(String(255), nullable=True)
    subject: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="new")
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
