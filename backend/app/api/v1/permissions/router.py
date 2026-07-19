"""Permission REST API routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.permission import PermissionPage, PermissionRead, PermissionUpdate, PermissionWrite
from app.services.permission import PermissionService

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.get("", response_model=PermissionPage, dependencies=[Depends(require("users:manage"))])
def list_permissions(
    search: str | None = None,
    is_active: bool | None = None,
    sort: str = Query(default="code"),
    direction: str = Query(default="asc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=24, ge=1, le=100),
    db: Session = Depends(get_db),
) -> PermissionPage:
    """List permissions with search, filtering, sorting, and pagination."""

    items, total = PermissionService(db).list(search, is_active, sort, direction, page, page_size)
    return PermissionPage(items=items, total=total, page=page, page_size=page_size)


@router.post("", response_model=PermissionRead, dependencies=[Depends(require("users:manage"))])
def create_permission(data: PermissionWrite, db: Session = Depends(get_db)) -> PermissionRead:
    """Create a permission."""

    return PermissionService(db).create(data.model_dump())


@router.get("/{uuid}", response_model=PermissionRead, dependencies=[Depends(require("users:manage"))])
def get_permission(uuid: str, db: Session = Depends(get_db)) -> PermissionRead:
    """Get a permission by public identifier."""

    return PermissionService(db).get(uuid)


@router.put("/{uuid}", response_model=PermissionRead, dependencies=[Depends(require("users:manage"))])
def update_permission(uuid: str, data: PermissionUpdate, db: Session = Depends(get_db)) -> PermissionRead:
    """Update a permission."""

    return PermissionService(db).update(uuid, data.model_dump())


@router.delete("/{uuid}", dependencies=[Depends(require("users:manage"))])
def delete_permission(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    """Soft-delete a permission."""

    PermissionService(db).delete(uuid)
    return {"deleted": True}
