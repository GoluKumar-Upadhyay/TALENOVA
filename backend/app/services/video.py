"""Video business validation and workflows."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.video import VideoRepository
from app.models.video import Video

class VideoService:
    """Coordinates video source validation and persistence."""
    SORT_FIELDS = set(VideoRepository.SORT_FIELDS)
    def __init__(self, db: Session) -> None: self.repository = VideoRepository(db)
    def list(self, search, category, featured, is_active, sort, direction, page, page_size):
        if sort not in self.SORT_FIELDS: raise HTTPException(status_code=422, detail="Unsupported video sort field")
        if direction not in {"asc", "desc"}: raise HTTPException(status_code=422, detail="Unsupported sort direction")
        return self.repository.list(search, category, featured, is_active, sort, direction, page, page_size)
    def get(self, uuid: str): return self._find(uuid)
    def create(self, values: dict): self._validate(values); return self.repository.create(values)
    def update(self, uuid: str, values: dict):
        item = self._find(uuid); self._validate(values); return self.repository.save(item, values)
    def delete(self, uuid: str) -> None: self.repository.save(self._find(uuid), {"is_deleted": True})
    def _find(self, uuid: str) -> Video:
        item = self.repository.get(uuid)
        if item is None: raise HTTPException(status_code=404, detail="Video not found")
        return item
    @staticmethod
    def _validate(values: dict) -> None:
        youtube = values.get("youtube_url")
        if youtube and not ("youtube.com" in youtube or "youtu.be" in youtube):
            raise HTTPException(status_code=422, detail="YouTube URL is invalid")
