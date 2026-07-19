"""Analytics activity events used for dashboard charts."""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import DateTime, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class AnalyticsEvent(Base):
    """An append-only event used for monthly dashboard metrics."""
    __tablename__ = "analytics_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    event_metadata: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
