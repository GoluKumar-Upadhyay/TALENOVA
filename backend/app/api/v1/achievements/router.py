"""Achievement REST API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.achievement import AchievementPage, AchievementRead, AchievementWrite
from app.services.achievement import AchievementService
router = APIRouter(prefix="/achievements", tags=["achievements"])
@router.get("", response_model=AchievementPage)
def list_achievements(search: str | None = None, achievement_type: str | None = None, featured: bool | None = None, is_active: bool | None = None, sort: str = Query("display_order"), direction: str = Query("asc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> AchievementPage:
    """List achievements in public display order."""
    items, total = AchievementService(db).list(search, achievement_type, featured, is_active, sort, direction, page, page_size)
    return AchievementPage(items=items, total=total, page=page, page_size=page_size)
@router.get("/{uuid}", response_model=AchievementRead)
def get_achievement(uuid: str, db: Session = Depends(get_db)) -> AchievementRead:
    """Get achievement by id."""
    return AchievementService(db).get(uuid)
@router.post("", response_model=AchievementRead, dependencies=[Depends(require("cms:write"))])
def create_achievement(data: AchievementWrite, db: Session = Depends(get_db)) -> AchievementRead:
    """Create achievement after its image is stored in Supabase."""
    return AchievementService(db).create(data.model_dump())
@router.put("/{uuid}", response_model=AchievementRead, dependencies=[Depends(require("cms:write"))])
def update_achievement(uuid: str, data: AchievementWrite, db: Session = Depends(get_db)) -> AchievementRead:
    """Update achievement."""
    return AchievementService(db).update(uuid, data.model_dump())
@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_achievement(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    """Soft-delete achievement."""
    AchievementService(db).delete(uuid)
    return {"deleted": True}
