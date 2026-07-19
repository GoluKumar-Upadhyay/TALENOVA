"""Gallery persistence operations."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.gallery import GalleryCategory, GalleryImage


class GalleryRepository:
    """Encapsulates gallery image database access."""
    IMAGE_SORT_FIELDS = {"alt_text": GalleryImage.alt_text, "display_order": GalleryImage.display_order, "created_at": GalleryImage.created_at}
    CATEGORY_SORT_FIELDS = {"name": GalleryCategory.name, "display_order": GalleryCategory.display_order, "created_at": GalleryCategory.created_at}

    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, search: str | None, category_id: int | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[GalleryImage], int]:
        """List gallery images with text and category filters."""
        filters = [GalleryImage.is_deleted.is_(False)]
        if search:
            filters.append(GalleryImage.alt_text.ilike(f"%{search}%"))
        if category_id:
            filters.append(GalleryImage.category_id == category_id)
        if is_active is not None:
            filters.append(GalleryImage.is_active == is_active)
        order = self.IMAGE_SORT_FIELDS[sort].desc() if direction == "desc" else self.IMAGE_SORT_FIELDS[sort].asc()
        statement = select(GalleryImage).where(*filters).order_by(order)
        items = list(self.db.scalars(statement.offset((page - 1) * page_size).limit(page_size)))
        total = self.db.scalar(select(func.count()).select_from(GalleryImage).where(*filters))
        return items, total or 0

    def get(self, uuid: str) -> GalleryImage | None:
        """Find a gallery image by public id."""
        return self.db.scalar(select(GalleryImage).where(GalleryImage.uuid == uuid, GalleryImage.is_deleted.is_(False)))

    def create(self, values: dict) -> GalleryImage:
        """Store a media URL record after upload validation."""
        item = GalleryImage(**values)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def save(self, item: GalleryImage, values: dict) -> GalleryImage:
        """Persist an image update."""
        for field, value in values.items():
            setattr(item, field, value)
        self.db.commit()
        self.db.refresh(item)
        return item
    def list_categories(self, search: str | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[GalleryCategory], int]:
        filters = [GalleryCategory.is_deleted.is_(False)]
        if search:
            filters.append(GalleryCategory.name.ilike(f"%{search}%"))
        if is_active is not None:
            filters.append(GalleryCategory.is_active == is_active)
        order = self.CATEGORY_SORT_FIELDS[sort].desc() if direction == "desc" else self.CATEGORY_SORT_FIELDS[sort].asc()
        query = select(GalleryCategory).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(GalleryCategory).where(*filters)) or 0
    def get_category(self, uuid: str) -> GalleryCategory | None:
        return self.db.scalar(select(GalleryCategory).where(GalleryCategory.uuid == uuid, GalleryCategory.is_deleted.is_(False)))

    def category_exists(self, category_id: int) -> bool:
        """Return True if a non-deleted gallery category with this PK exists."""
        return self.db.scalar(
            select(func.count()).select_from(GalleryCategory).where(
                GalleryCategory.id == category_id,
                GalleryCategory.is_deleted.is_(False),
            )
        ) > 0
    def create_category(self, values: dict) -> GalleryCategory:
        item = GalleryCategory(**values); self.db.add(item); self.db.commit(); self.db.refresh(item); return item
    def save_category(self, item: GalleryCategory, values: dict) -> GalleryCategory:
        for field, value in values.items():
            setattr(item, field, value)
        self.db.commit(); self.db.refresh(item); return item
