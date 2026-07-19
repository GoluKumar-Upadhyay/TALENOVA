"""Founder profile routes."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.founder import FounderPage, FounderRead, FounderWrite
from app.services.founder import FounderService

router = APIRouter(prefix="/founders", tags=["founders"])


@router.get("", response_model=FounderPage)
def list_founders(search: str | None = None, founder_type: str | None = None, is_active: bool | None = True, sort: str = Query("display_order"), direction: str = Query("asc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> FounderPage:
    """Return active leadership profiles ordered for public display."""

    items, total = FounderService(db).list(search, founder_type, is_active, sort, direction, page, page_size)
    return FounderPage(items=items, total=total, page=page, page_size=page_size)


@router.post("", response_model=FounderRead, dependencies=[Depends(require("cms:write"))])
def create_founder(data: FounderWrite, db: Session = Depends(get_db)) -> FounderRead:
    """Create a leadership role profile."""

    return FounderService(db).create(data.model_dump())


@router.get("/{uuid}", response_model=FounderRead)
def get_founder(uuid: str, db: Session = Depends(get_db)) -> FounderRead:
    """Get one leadership role profile."""

    return FounderService(db).get(uuid)


@router.put("/id/{uuid}", response_model=FounderRead, dependencies=[Depends(require("cms:write"))])
def update_founder(uuid: str, data: FounderWrite, db: Session = Depends(get_db)) -> FounderRead:
    """Update one leadership role profile by id."""

    return FounderService(db).update(uuid, data.model_dump())


@router.put("/{founder_type}", response_model=FounderRead, dependencies=[Depends(require("cms:write"))])
def save_founder(founder_type: str, data: FounderWrite, db: Session = Depends(get_db)) -> FounderRead:
    """Create or replace one leadership role profile."""

    if founder_type != data.founder_type:
        raise HTTPException(status_code=422, detail="Founder type does not match path")
    return FounderService(db).save(founder_type, data.model_dump())


@router.delete("/{uuid}", response_model=FounderRead, dependencies=[Depends(require("cms:write"))])
def delete_founder(uuid: str, db: Session = Depends(get_db)) -> FounderRead:
    """Soft-delete one leadership role profile."""

    return FounderService(db).delete(uuid)
