"""Database access for founder and co-founder profiles."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.founder import Founder


class FounderRepository:
    """Encapsulates persistence operations for leadership profiles."""
    SORT_FIELDS = {"name": Founder.name, "founder_type": Founder.founder_type, "display_order": Founder.display_order, "created_at": Founder.created_at}

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[Founder]:
        """Return public leadership profiles in display order."""

        statement = (
            select(Founder)
            .where(Founder.is_deleted.is_(False), Founder.is_active.is_(True))
            .order_by(Founder.display_order)
        )
        return list(self.db.scalars(statement))

    def list(self, search: str | None, founder_type: str | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[Founder], int]:
        filters = [Founder.is_deleted.is_(False)]
        if search:
            filters.append(Founder.name.ilike(f"%{search}%"))
        if founder_type:
            filters.append(Founder.founder_type == founder_type)
        if is_active is not None:
            filters.append(Founder.is_active == is_active)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(Founder).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(Founder).where(*filters)) or 0

    def get(self, uuid: str) -> Founder | None:
        return self.db.scalar(select(Founder).where(Founder.uuid == uuid, Founder.is_deleted.is_(False)))

    def get_by_type(self, founder_type: str) -> Founder | None:
        """Get a non-deleted founder record by its unique role type."""

        return self.db.scalar(
            select(Founder).where(
                Founder.founder_type == founder_type,
                Founder.is_deleted.is_(False),
            )
        )

    def create(self, values: dict) -> Founder:
        """Persist a new leadership profile transactionally."""

        founder = Founder(**values)
        self.db.add(founder)
        self.db.commit()
        self.db.refresh(founder)
        return founder

    def update(self, founder: Founder, values: dict) -> Founder:
        """Persist an allowed leadership profile update."""

        for field, value in values.items():
            setattr(founder, field, value)
        self.db.commit()
        self.db.refresh(founder)
        return founder
