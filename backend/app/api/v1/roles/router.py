"""Role REST API routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.role import RolePage, RoleRead, RoleUpdate, RoleWrite
from app.services.role import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=RolePage, dependencies=[Depends(require("users:manage"))])
def list_roles(
    search: str | None = None,
    is_active: bool | None = None,
    permission_code: str | None = None,
    sort: str = Query(default="name"),
    direction: str = Query(default="asc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=24, ge=1, le=100),
    db: Session = Depends(get_db),
) -> RolePage:
    """List roles with search, filtering, sorting, and pagination."""

    items, total = RoleService(db).list(search, is_active, permission_code, sort, direction, page, page_size)
    return RolePage(items=items, total=total, page=page, page_size=page_size)


@router.post("", response_model=RoleRead, dependencies=[Depends(require("users:manage"))])
def create_role(data: RoleWrite, db: Session = Depends(get_db)) -> RoleRead:
    """Create a role."""

    return RoleService(db).create(data.model_dump())


@router.get("/{uuid}", response_model=RoleRead, dependencies=[Depends(require("users:manage"))])
def get_role(uuid: str, db: Session = Depends(get_db)) -> RoleRead:
    """Get a role by public identifier."""

    return RoleService(db).get(uuid)


@router.put("/{uuid}", response_model=RoleRead, dependencies=[Depends(require("users:manage"))])
def update_role(uuid: str, data: RoleUpdate, db: Session = Depends(get_db)) -> RoleRead:
    """Update a role."""

    return RoleService(db).update(uuid, data.model_dump())


@router.delete("/{uuid}", dependencies=[Depends(require("users:manage"))])
def delete_role(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    """Soft-delete a role."""

    RoleService(db).delete(uuid)
    return {"deleted": True}


@router.post("/{uuid}/permissions/{permission_uuid}", response_model=RoleRead, dependencies=[Depends(require("users:manage"))])
def attach_permission(uuid: str, permission_uuid: str, db: Session = Depends(get_db)) -> RoleRead:
    """Assign a permission to a role."""

    return RoleService(db).attach_permission(uuid, permission_uuid)


@router.delete("/{uuid}/permissions/{permission_uuid}", response_model=RoleRead, dependencies=[Depends(require("users:manage"))])
def detach_permission(uuid: str, permission_uuid: str, db: Session = Depends(get_db)) -> RoleRead:
    """Remove a permission from a role."""

    return RoleService(db).detach_permission(uuid, permission_uuid)
