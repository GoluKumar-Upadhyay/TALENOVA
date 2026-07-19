"""User REST API routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.user import UserPage, UserRead, UserUpdate, UserWrite
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=UserPage, dependencies=[Depends(require("users:manage"))])
def list_users(
    search: str | None = None,
    role: str | None = None,
    is_active: bool | None = None,
    is_email_verified: bool | None = None,
    sort: str = Query(default="created_at"),
    direction: str = Query(default="desc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=24, ge=1, le=100),
    db: Session = Depends(get_db),
) -> UserPage:
    """List users with search, filtering, sorting, and pagination."""

    items, total = UserService(db).list(search, role, is_active, is_email_verified, sort, direction, page, page_size)
    return UserPage(items=items, total=total, page=page, page_size=page_size)


@router.post("", response_model=UserRead, dependencies=[Depends(require("users:manage"))])
def create_user(data: UserWrite, db: Session = Depends(get_db)) -> UserRead:
    """Create a user."""

    return UserService(db).create(data.model_dump())


@router.get("/{uuid}", response_model=UserRead, dependencies=[Depends(require("users:manage"))])
def get_user(uuid: str, db: Session = Depends(get_db)) -> UserRead:
    """Get a user by public identifier."""

    return UserService(db).get(uuid)


@router.put("/{uuid}", response_model=UserRead, dependencies=[Depends(require("users:manage"))])
def update_user(uuid: str, data: UserUpdate, db: Session = Depends(get_db)) -> UserRead:
    """Update a user."""

    return UserService(db).update(uuid, data.model_dump())


@router.delete("/{uuid}", dependencies=[Depends(require("users:manage"))])
def delete_user(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    """Soft-delete a user."""

    UserService(db).delete(uuid)
    return {"deleted": True}


@router.post("/{uuid}/roles/{role_uuid}", response_model=UserRead, dependencies=[Depends(require("users:manage"))])
def attach_role(uuid: str, role_uuid: str, db: Session = Depends(get_db)) -> UserRead:
    """Assign a role to a user."""

    return UserService(db).attach_role(uuid, role_uuid)


@router.delete("/{uuid}/roles/{role_uuid}", response_model=UserRead, dependencies=[Depends(require("users:manage"))])
def detach_role(uuid: str, role_uuid: str, db: Session = Depends(get_db)) -> UserRead:
    """Remove a role from a user."""

    return UserService(db).detach_role(uuid, role_uuid)
