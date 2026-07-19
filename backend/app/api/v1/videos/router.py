"""Video REST API routes."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.video import VideoPage, VideoRead, VideoWrite
from app.services.video import VideoService
router = APIRouter(prefix="/videos", tags=["videos"])
@router.get("", response_model=VideoPage)
def list_videos(search: str | None = None, category: str | None = None, featured: bool | None = None, is_active: bool | None = None, sort: str = Query("display_order"), direction: str = Query("asc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> VideoPage:
    """List searchable and filterable videos."""
    items, total = VideoService(db).list(search, category, featured, is_active, sort, direction, page, page_size)
    return VideoPage(items=items, total=total, page=page, page_size=page_size)
@router.get("/{uuid}", response_model=VideoRead)
def get_video(uuid: str, db: Session = Depends(get_db)) -> VideoRead:
    """Get video by id."""
    return VideoService(db).get(uuid)
@router.post("", response_model=VideoRead, dependencies=[Depends(require("cms:write"))])
def create_video(data: VideoWrite, db: Session = Depends(get_db)) -> VideoRead:
    """Create a video record after remote media upload."""
    return VideoService(db).create(data.model_dump())
@router.put("/{uuid}", response_model=VideoRead, dependencies=[Depends(require("cms:write"))])
def update_video(uuid: str, data: VideoWrite, db: Session = Depends(get_db)) -> VideoRead:
    """Update a video record."""
    return VideoService(db).update(uuid, data.model_dump())
@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_video(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    """Soft-delete a video record."""
    VideoService(db).delete(uuid); return {"deleted": True}
