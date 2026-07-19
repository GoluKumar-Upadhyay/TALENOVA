"""Partner REST routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.partner import PartnerPage, PartnerRead, PartnerWrite
from app.services.partner import PartnerService

router = APIRouter(prefix="/partners", tags=["partners"])


@router.get("", response_model=PartnerPage)
def list_partners(
    search: str | None = None,
    partner_type: str | None = None,
    is_active: bool | None = None,
    sort: str = Query(default="display_order"),
    direction: str = Query(default="asc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=24, ge=1, le=100),
    db: Session = Depends(get_db),
) -> PartnerPage:
    """List partners with optional search and type filter."""

    items, total = PartnerService(db).list(search, partner_type, is_active, sort, direction, page, page_size)
    return PartnerPage(items=items, total=total, page=page, page_size=page_size)


@router.get("/{uuid}", response_model=PartnerRead)
def get_partner(uuid: str, db: Session = Depends(get_db)) -> PartnerRead:
    """Get a partner profile."""

    return PartnerService(db).get(uuid)


@router.post("", response_model=PartnerRead, dependencies=[Depends(require("cms:write"))])
def create_partner(data: PartnerWrite, db: Session = Depends(get_db)) -> PartnerRead:
    """Create a partner profile."""

    return PartnerService(db).create(data.model_dump())


@router.put("/{uuid}", response_model=PartnerRead, dependencies=[Depends(require("cms:write"))])
def update_partner(uuid: str, data: PartnerWrite, db: Session = Depends(get_db)) -> PartnerRead:
    """Update a partner profile."""

    return PartnerService(db).update(uuid, data.model_dump())


@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_partner(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    """Soft-delete a partner profile."""

    PartnerService(db).delete(uuid)
    return {"deleted": True}
