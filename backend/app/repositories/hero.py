"""Hero section and statistic persistence operations."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.hero import HeroSection, Statistic


class HeroRepository:
    """Database access for homepage hero sections and statistics."""

    HERO_SORT_FIELDS = {"heading": HeroSection.heading, "created_at": HeroSection.created_at, "updated_at": HeroSection.updated_at}
    STAT_SORT_FIELDS = {"label": Statistic.label, "display_order": Statistic.display_order, "created_at": Statistic.created_at}

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_heroes(self, search: str | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        filters = []
        if search:
            filters.append(HeroSection.heading.ilike(f"%{search}%"))
        if is_active is not None:
            filters.append(HeroSection.is_active == is_active)
        order = self.HERO_SORT_FIELDS[sort].desc() if direction == "desc" else self.HERO_SORT_FIELDS[sort].asc()
        query = select(HeroSection).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(HeroSection).where(*filters)) or 0

    def get_hero(self, uuid: str) -> HeroSection | None:
        return self.db.scalar(select(HeroSection).where(HeroSection.uuid == uuid))

    def save_hero(self, item: HeroSection, values: dict) -> HeroSection:
        for field, value in values.items():
            setattr(item, field, value)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_hero(self, item: HeroSection) -> None:
        self.db.delete(item)
        self.db.commit()

    def list_statistics(self, search: str | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        filters = []
        if search:
            filters.append(Statistic.label.ilike(f"%{search}%"))
        if is_active is not None:
            filters.append(Statistic.is_active == is_active)
        order = self.STAT_SORT_FIELDS[sort].desc() if direction == "desc" else self.STAT_SORT_FIELDS[sort].asc()
        query = select(Statistic).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(Statistic).where(*filters)) or 0

    def get_statistic(self, uuid: str) -> Statistic | None:
        return self.db.scalar(select(Statistic).where(Statistic.uuid == uuid))

    def save_statistic(self, item: Statistic, values: dict) -> Statistic:
        for field, value in values.items():
            setattr(item, field, value)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_statistic(self, item: Statistic) -> None:
        self.db.delete(item)
        self.db.commit()
