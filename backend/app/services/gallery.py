"""Gallery business rules."""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.gallery import GalleryRepository


class GalleryService:
    """Coordinates gallery record validation and persistence."""
    IMAGE_SORT_FIELDS = set(GalleryRepository.IMAGE_SORT_FIELDS)
    CATEGORY_SORT_FIELDS = set(GalleryRepository.CATEGORY_SORT_FIELDS)

    def __init__(self, db: Session) -> None:
        self.repository = GalleryRepository(db)

    def list(self, search: str | None, category_id: int | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        """Return a paginated gallery image collection."""
        if sort not in self.IMAGE_SORT_FIELDS:
            raise HTTPException(status_code=422, detail="Unsupported gallery sort field")
        if direction not in {"asc", "desc"}:
            raise HTTPException(status_code=422, detail="Unsupported sort direction")
        return self.repository.list(search, category_id, is_active, sort, direction, page, page_size)
    def get(self, uuid: str):
        return self._find(uuid)

    def create(self, values: dict):
        """Create a gallery record for an uploaded Supabase URL."""
        self._validate_storage_url(values["image_url"])
        return self.repository.create(values)

    def update(self, uuid: str, values: dict):
        """Update a gallery record after validating its image URL."""
        item = self._find(uuid)
        self._validate_storage_url(values["image_url"])
        return self.repository.save(item, values)

    def delete(self, uuid: str) -> None:
        """Soft-delete a gallery image record."""
        self.repository.save(self._find(uuid), {"is_deleted": True})
    def list_categories(self, search: str | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int):
        if sort not in self.CATEGORY_SORT_FIELDS:
            raise HTTPException(status_code=422, detail="Unsupported gallery category sort field")
        if direction not in {"asc", "desc"}:
            raise HTTPException(status_code=422, detail="Unsupported sort direction")
        return self.repository.list_categories(search, is_active, sort, direction, page, page_size)
    def get_category(self, uuid: str):
        item = self.repository.get_category(uuid)
        if item is None:
            raise HTTPException(status_code=404, detail="Gallery category not found")
        return item
    def create_category(self, values: dict):
        return self.repository.create_category(values)
    def update_category(self, uuid: str, values: dict):
        return self.repository.save_category(self.get_category(uuid), values)
    def delete_category(self, uuid: str):
        self.repository.save_category(self.get_category(uuid), {"is_deleted": True})

    def _find(self, uuid: str):
        item = self.repository.get(uuid)
        if item is None:
            raise HTTPException(status_code=404, detail="Gallery image not found")
        return item

    @staticmethod
    def _validate_storage_url(url: str) -> None:
        """Reject non-HTTPS image locations before persistence."""
        if not url.startswith("https://"):
            raise HTTPException(status_code=422, detail="Image URL must use HTTPS")
