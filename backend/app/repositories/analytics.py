"""Optimised dashboard aggregate queries."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.analytics import AnalyticsEvent

# Entity tables for live counts — use the actual class names from each module
from app.models.course import Course
from app.models.teacher import Teacher
from app.models.contact import ContactMessage
from app.models.event import WorkshopEvent
from app.models.internship import InternshipProgram
from app.models.testimonial import Testimonial
from app.models.success_story import SuccessStory
from app.models.gallery import GalleryImage
from app.models.video import Video


class AnalyticsRepository:
    """Reads aggregate counts from entity tables and recent activity events."""

    SORT_FIELDS = {
        "event_type": AnalyticsEvent.event_type,
        "occurred_at": AnalyticsEvent.occurred_at,
    }

    def __init__(self, db: Session) -> None:
        self.db = db

    # ── Dashboard live counts ────────────────────────────────────────────────

    def live_counts(self) -> dict[str, int]:
        """Return real row counts from every entity table (excludes soft-deleted rows)."""

        def _count_soft(model) -> int:
            """COUNT rows where is_deleted IS false."""
            return self.db.scalar(
                select(func.count()).select_from(model).where(model.is_deleted.is_(False))
            ) or 0

        return {
            "courses":         _count_soft(Course),
            "teachers":        _count_soft(Teacher),
            # ContactMessage has no is_deleted — count all rows
            "contacts":        self.db.scalar(
                                   select(func.count()).select_from(ContactMessage)
                               ) or 0,
            "events":          _count_soft(WorkshopEvent),
            "internships":     _count_soft(InternshipProgram),
            "testimonials":    _count_soft(Testimonial),
            "success_stories": _count_soft(SuccessStory),
            "gallery_images":  _count_soft(GalleryImage),
            "videos":          _count_soft(Video),
            # students not yet modelled → always 0
            "students":        0,
        }

    # ── Analytics event queries (unchanged) ─────────────────────────────────

    def event_counts(self, start=None, end=None) -> list[tuple[str, int]]:
        filters = []
        if start:
            filters.append(AnalyticsEvent.occurred_at >= start)
        if end:
            filters.append(AnalyticsEvent.occurred_at <= end)
        query = (
            select(AnalyticsEvent.event_type, func.count())
            .where(*filters)
            .group_by(AnalyticsEvent.event_type)
        )
        return list(self.db.execute(query))

    def recent(self, limit: int = 10) -> list[AnalyticsEvent]:
        return list(
            self.db.scalars(
                select(AnalyticsEvent)
                .order_by(AnalyticsEvent.occurred_at.desc())
                .limit(limit)
            )
        )

    def list(
        self,
        search: str | None,
        event_type: str | None,
        start=None,
        end=None,
        sort: str = "occurred_at",
        direction: str = "desc",
        page: int = 1,
        page_size: int = 24,
    ):
        filters = []
        if search:
            filters.append(AnalyticsEvent.event_type.ilike(f"%{search}%"))
        if event_type:
            filters.append(AnalyticsEvent.event_type == event_type)
        if start:
            filters.append(AnalyticsEvent.occurred_at >= start)
        if end:
            filters.append(AnalyticsEvent.occurred_at <= end)
        order = (
            self.SORT_FIELDS[sort].desc()
            if direction == "desc"
            else self.SORT_FIELDS[sort].asc()
        )
        query = select(AnalyticsEvent).where(*filters).order_by(order)
        return (
            list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))),
            self.db.scalar(
                select(func.count()).select_from(AnalyticsEvent).where(*filters)
            ) or 0,
        )

    def get(self, uuid: str) -> AnalyticsEvent | None:
        return self.db.scalar(select(AnalyticsEvent).where(AnalyticsEvent.uuid == uuid))

    def save(self, item: AnalyticsEvent, values: dict) -> AnalyticsEvent:
        for key, value in values.items():
            setattr(item, key, value)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: AnalyticsEvent) -> None:
        self.db.delete(item)
        self.db.commit()
