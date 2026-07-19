"""User business operations."""

from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository

passwords = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class UserService:
    """Coordinates user validation, password hashing, and role assignment."""

    SORT_FIELDS = {"email", "full_name", "created_at", "updated_at", "last_login_at"}
    SORT_DIRECTIONS = {"asc", "desc"}

    def __init__(self, db: Session) -> None:
        self.repository = UserRepository(db)
        self.role_repository = RoleRepository(db)

    def list(
        self,
        search: str | None,
        role: str | None,
        is_active: bool | None,
        is_email_verified: bool | None,
        sort: str,
        direction: str,
        page: int,
        page_size: int,
    ):
        self._validate_sort(sort, direction)
        return self.repository.list(search, role, is_active, is_email_verified, sort, direction, page, page_size)

    def get(self, uuid: str):
        user = self.repository.get(uuid)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_by_email(self, email: str):
        return self.repository.get_by_email(email.lower())

    def create(self, values: dict):
        role_uuids = values.pop("role_uuids", [])
        email = str(values["email"]).lower()
        if self.repository.get_by_email(email):
            raise HTTPException(status_code=409, detail="Email already exists")
        roles = self._roles(role_uuids)
        password = values.pop("password")
        values["email"] = email
        values["password_hash"] = passwords.hash(password)
        if values.get("is_email_verified"):
            values["email_verified_at"] = datetime.utcnow()
        return self.repository.create(values, roles)

    def update(self, uuid: str, values: dict):
        user = self.get(uuid)
        role_uuids = values.pop("role_uuids", None)
        values = {key: value for key, value in values.items() if value is not None}
        if "email" in values:
            values["email"] = str(values["email"]).lower()
            existing = self.repository.get_by_email(values["email"])
            if existing and existing.uuid != uuid:
                raise HTTPException(status_code=409, detail="Email already exists")
        if "password" in values:
            values["password_hash"] = passwords.hash(values.pop("password"))
        if values.get("is_email_verified") and not user.email_verified_at:
            values["email_verified_at"] = datetime.utcnow()
        if values.get("is_email_verified") is False:
            values["email_verified_at"] = None
        roles = self._roles(role_uuids) if role_uuids is not None else None
        return self.repository.update(user, values, roles)

    def delete(self, uuid: str) -> None:
        self.repository.delete(self.get(uuid))

    def attach_role(self, user_uuid: str, role_uuid: str):
        user = self.get(user_uuid)
        role = self.role_repository.get(role_uuid)
        if role is None:
            raise HTTPException(status_code=404, detail="Role not found")
        if role not in user.roles:
            user.roles.append(role)
        self.repository.db.commit()
        return self.repository.get(user.uuid)

    def detach_role(self, user_uuid: str, role_uuid: str):
        user = self.get(user_uuid)
        role = self.role_repository.get(role_uuid)
        if role is None:
            raise HTTPException(status_code=404, detail="Role not found")
        user.roles = [item for item in user.roles if item.uuid != role_uuid]
        self.repository.db.commit()
        return self.repository.get(user.uuid)

    def _roles(self, role_uuids: list[str]) -> list:
        roles = self.role_repository.get_many(role_uuids)
        if len(roles) != len(set(role_uuids)):
            raise HTTPException(status_code=422, detail="One or more roles do not exist")
        return roles

    def _validate_sort(self, sort: str, direction: str) -> None:
        if sort not in self.SORT_FIELDS:
            raise HTTPException(status_code=422, detail="Unsupported user sort field")
        if direction not in self.SORT_DIRECTIONS:
            raise HTTPException(status_code=422, detail="Unsupported sort direction")
