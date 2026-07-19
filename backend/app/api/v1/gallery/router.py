"""Public gallery image listing API."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.v1.auth.router import require
from app.schemas.gallery import GalleryCategoryPage, GalleryCategoryRead, GalleryCategoryWrite, GalleryImagePage, GalleryImageRead, GalleryImageWrite
from app.services.gallery import GalleryService

router = APIRouter(prefix="/gallery", tags=["gallery"])


@router.get("", response_model=GalleryImagePage)
def list_gallery(
    category_id: int | None = None,
    search: str | None = None,
    is_active: bool | None = True,
    sort: str = Query(default="display_order"),
    direction: str = Query(default="asc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=24, ge=1, le=100),
    db: Session = Depends(get_db),
) -> GalleryImagePage:
    """List active gallery images for responsive grids and lightboxes."""
    items, total = GalleryService(db).list(search, category_id, is_active, sort, direction, page, page_size)
    return GalleryImagePage(items=items, total=total, page=page, page_size=page_size)


@router.get("/categories", response_model=GalleryCategoryPage)
def list_gallery_categories(search: str | None = None, is_active: bool | None = True, sort: str = Query(default="display_order"), direction: str = Query(default="asc"), page: int = Query(default=1, ge=1), page_size: int = Query(default=24, ge=1, le=100), db: Session = Depends(get_db)) -> GalleryCategoryPage:
    """List gallery categories."""
    items, total = GalleryService(db).list_categories(search, is_active, sort, direction, page, page_size)
    return GalleryCategoryPage(items=items, total=total, page=page, page_size=page_size)


@router.post("/categories", response_model=GalleryCategoryRead, dependencies=[Depends(require("cms:write"))])
def create_gallery_category(data: GalleryCategoryWrite, db: Session = Depends(get_db)) -> GalleryCategoryRead:
    return GalleryService(db).create_category(data.model_dump())


@router.get("/categories/{uuid}", response_model=GalleryCategoryRead)
def get_gallery_category(uuid: str, db: Session = Depends(get_db)) -> GalleryCategoryRead:
    return GalleryService(db).get_category(uuid)


@router.put("/categories/{uuid}", response_model=GalleryCategoryRead, dependencies=[Depends(require("cms:write"))])
def update_gallery_category(uuid: str, data: GalleryCategoryWrite, db: Session = Depends(get_db)) -> GalleryCategoryRead:
    return GalleryService(db).update_category(uuid, data.model_dump())


@router.delete("/categories/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_gallery_category(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    GalleryService(db).delete_category(uuid); return {"deleted": True}


@router.get("/admin", response_model=GalleryImagePage, dependencies=[Depends(require("cms:write"))])
def list_gallery_admin(search: str | None = None, category_id: int | None = None, is_active: bool | None = None, sort: str = Query(default="display_order"), direction: str = Query(default="asc"), page: int = Query(default=1, ge=1), page_size: int = Query(default=100, ge=1, le=100), db: Session = Depends(get_db)) -> GalleryImagePage:
    """List all gallery records for the CMS."""
    items, total = GalleryService(db).list(search, category_id, is_active, sort, direction, page, page_size)
    return GalleryImagePage(items=items, total=total, page=page, page_size=page_size)


@router.get("/{uuid}", response_model=GalleryImageRead)
def get_gallery_image(uuid: str, db: Session = Depends(get_db)) -> GalleryImageRead:
    return GalleryService(db).get(uuid)


@router.post("", response_model=GalleryImageRead, dependencies=[Depends(require("cms:write"))])
def create_gallery_image(data: GalleryImageWrite, db: Session = Depends(get_db)) -> GalleryImageRead:
    """Create a gallery image record after Supabase upload."""
    return GalleryService(db).create(data.model_dump())


@router.put("/{uuid}", response_model=GalleryImageRead, dependencies=[Depends(require("cms:write"))])
def update_gallery_image(uuid: str, data: GalleryImageWrite, db: Session = Depends(get_db)) -> GalleryImageRead:
    """Update an existing gallery image."""
    return GalleryService(db).update(uuid, data.model_dump())


@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_gallery_image(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    """Soft-delete a gallery image."""
    GalleryService(db).delete(uuid)
    return {"deleted": True}
