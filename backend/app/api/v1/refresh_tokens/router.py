"""Refresh token administrative REST API routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.refresh_token import RefreshTokenPage, RefreshTokenRead
from app.services.refresh_token import RefreshTokenService

router = APIRouter(prefix="/refresh-tokens", tags=["refresh-tokens"])


@router.get("", response_model=RefreshTokenPage, dependencies=[Depends(require("users:manage"))])
def list_refresh_tokens(
    search: str | None = None,
    user_uuid: str | None = None,
    status: str | None = None,
    sort: str = Query(default="created_at"),
    direction: str = Query(default="desc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=24, ge=1, le=100),
    db: Session = Depends(get_db),
) -> RefreshTokenPage:
    """List refresh tokens with search, filtering, sorting, and pagination."""

    service = RefreshTokenService(db)
    items, total = service.list(search, user_uuid, status, sort, direction, page, page_size)
    return RefreshTokenPage(items=[service.serialize(item) for item in items], total=total, page=page, page_size=page_size)


@router.get("/{uuid}", response_model=RefreshTokenRead, dependencies=[Depends(require("users:manage"))])
def get_refresh_token(uuid: str, db: Session = Depends(get_db)) -> RefreshTokenRead:
    """Get a refresh token by public identifier."""

    service = RefreshTokenService(db)
    return service.serialize(service.get(uuid))


@router.post("/{uuid}/revoke", response_model=RefreshTokenRead, dependencies=[Depends(require("users:manage"))])
def revoke_refresh_token(uuid: str, db: Session = Depends(get_db)) -> RefreshTokenRead:
    """Revoke a refresh token."""

    service = RefreshTokenService(db)
    return service.serialize(service.revoke(uuid))


@router.delete("/{uuid}", dependencies=[Depends(require("users:manage"))])
def delete_refresh_token(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    """Revoke a refresh token through the CRUD delete route."""

    RefreshTokenService(db).revoke(uuid)
    return {"deleted": True}
