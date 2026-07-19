"""Partner database access layer."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.partner import Partner


class PartnerRepository:
    """Persistence operations for partners."""
    SORT_FIELDS = {"name": Partner.name, "partner_type": Partner.partner_type, "display_order": Partner.display_order, "created_at": Partner.created_at}

    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, search: str | None, partner_type: str | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[Partner], int]:
        """Find partners using optional text and type filters."""

        filters = [Partner.is_deleted.is_(False)]
        if search:
            filters.append(Partner.name.ilike(f"%{search}%"))
        if partner_type:
            filters.append(Partner.partner_type == partner_type)
        if is_active is not None:
            filters.append(Partner.is_active == is_active)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        statement = select(Partner).where(*filters).order_by(order)
        items = list(self.db.scalars(statement.offset((page - 1) * page_size).limit(page_size)))
        total = self.db.scalar(select(func.count()).select_from(Partner).where(*filters))
        return items, total or 0

    def get(self, uuid: str) -> Partner | None:
        """Get a non-deleted partner by public id."""

        return self.db.scalar(select(Partner).where(Partner.uuid == uuid, Partner.is_deleted.is_(False)))

    def create(self, values: dict) -> Partner:
        """Persist a partner record."""

        item = Partner(**values)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: Partner, values: dict) -> Partner:
        """Persist a mutation of a partner record."""

        for field, value in values.items():
            setattr(item, field, value)
        self.db.commit()
        self.db.refresh(item)
        return item
