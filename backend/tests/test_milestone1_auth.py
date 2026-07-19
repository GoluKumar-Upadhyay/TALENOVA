"""Milestone 1 backend coverage for authentication, users, RBAC, and tokens."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import auth
from app.models.auth import Permission, Role, User
from app.services.user import passwords


AUTH_TABLES = [
    auth.User.__table__,
    auth.Role.__table__,
    auth.Permission.__table__,
    auth.user_roles,
    auth.role_permissions,
    auth.RefreshToken.__table__,
    auth.PasswordResetToken.__table__,
    auth.EmailVerificationToken.__table__,
]


@pytest.fixture
def db() -> Iterator[Session]:
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine, tables=AUTH_TABLES)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine, tables=list(reversed(AUTH_TABLES)))
        engine.dispose()


@pytest.fixture
def client(db: Session) -> Iterator[TestClient]:
    def override_db() -> Iterator[Session]:
        yield db

    app.dependency_overrides[get_db] = override_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def seed_admin(db: Session) -> User:
    permission = Permission(code="users:manage", name="Manage Users")
    role = Role(name="admin", description="Administrator", permissions=[permission])
    user = User(
        email="admin@example.com",
        password_hash=passwords.hash("AdminPass1"),
        full_name="Admin User",
        is_email_verified=True,
        roles=[role],
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def admin_headers(client: TestClient, db: Session) -> dict[str, str]:
    seed_admin(db)
    response = client.post("/api/v1/auth/login", json={"email": "admin@example.com", "password": "AdminPass1"})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_login_me_refresh_and_logout_flow(client: TestClient, db: Session) -> None:
    seed_admin(db)

    login = client.post("/api/v1/auth/login", json={"email": "admin@example.com", "password": "AdminPass1"})
    assert login.status_code == 200
    tokens = login.json()

    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"})
    assert me.status_code == 200
    assert me.json()["email"] == "admin@example.com"

    refreshed = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert refreshed.status_code == 200
    assert refreshed.json()["refresh_token"] != tokens["refresh_token"]

    old_refresh = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert old_refresh.status_code == 401

    logout = client.post("/api/v1/auth/logout", json={"refresh_token": refreshed.json()["refresh_token"]})
    assert logout.status_code == 200

    logged_out_refresh = client.post("/api/v1/auth/refresh", json={"refresh_token": refreshed.json()["refresh_token"]})
    assert logged_out_refresh.status_code == 401


def test_users_roles_permissions_crud_search_filter_sort_and_pagination(client: TestClient, db: Session) -> None:
    headers = admin_headers(client, db)

    permission = client.post(
        "/api/v1/permissions",
        headers=headers,
        json={"code": "students:read", "name": "Read Students", "description": "View student records"},
    )
    assert permission.status_code == 200
    permission_uuid = permission.json()["uuid"]

    permissions = client.get(
        "/api/v1/permissions?search=students&is_active=true&sort=code&direction=asc&page=1&page_size=10",
        headers=headers,
    )
    assert permissions.status_code == 200
    assert permissions.json()["total"] == 1

    role = client.post(
        "/api/v1/roles",
        headers=headers,
        json={"name": "mentor", "description": "Mentor role", "permission_uuids": [permission_uuid]},
    )
    assert role.status_code == 200
    role_uuid = role.json()["uuid"]

    roles = client.get(
        "/api/v1/roles?search=mentor&permission_code=students:read&sort=name&direction=asc&page=1&page_size=10",
        headers=headers,
    )
    assert roles.status_code == 200
    assert roles.json()["items"][0]["name"] == "mentor"

    user = client.post(
        "/api/v1/users",
        headers=headers,
        json={
            "email": "student@example.com",
            "password": "StudentPass1",
            "full_name": "Student One",
            "role_uuids": [role_uuid],
        },
    )
    assert user.status_code == 200
    user_uuid = user.json()["uuid"]

    users = client.get(
        "/api/v1/users?search=student&role=mentor&is_active=true&sort=email&direction=asc&page=1&page_size=10",
        headers=headers,
    )
    assert users.status_code == 200
    assert users.json()["total"] == 1

    updated = client.put(
        f"/api/v1/users/{user_uuid}",
        headers=headers,
        json={"full_name": "Student Updated", "is_email_verified": True},
    )
    assert updated.status_code == 200
    assert updated.json()["full_name"] == "Student Updated"
    assert updated.json()["is_email_verified"] is True

    detached = client.delete(f"/api/v1/users/{user_uuid}/roles/{role_uuid}", headers=headers)
    assert detached.status_code == 200
    assert detached.json()["roles"] == []

    reattached = client.post(f"/api/v1/users/{user_uuid}/roles/{role_uuid}", headers=headers)
    assert reattached.status_code == 200
    assert reattached.json()["roles"][0]["name"] == "mentor"

    assert client.delete(f"/api/v1/users/{user_uuid}", headers=headers).status_code == 200
    assert client.delete(f"/api/v1/roles/{role_uuid}", headers=headers).status_code == 200
    assert client.delete(f"/api/v1/permissions/{permission_uuid}", headers=headers).status_code == 200


def test_forgot_reset_password_and_email_verification(client: TestClient, db: Session) -> None:
    headers = admin_headers(client, db)
    created = client.post(
        "/api/v1/users",
        headers=headers,
        json={"email": "verify@example.com", "password": "VerifyPass1", "full_name": "Verify User"},
    )
    assert created.status_code == 200

    verification = client.post("/api/v1/auth/email-verification", json={"email": "verify@example.com"})
    assert verification.status_code == 200
    verified = client.post("/api/v1/auth/verify-email", json={"token": verification.json()["verification_token"]})
    assert verified.status_code == 200

    user = client.get(f"/api/v1/users/{created.json()['uuid']}", headers=headers)
    assert user.json()["is_email_verified"] is True

    forgot = client.post("/api/v1/auth/forgot-password", json={"email": "verify@example.com"})
    assert forgot.status_code == 200

    reset = client.post(
        "/api/v1/auth/reset-password",
        json={"token": forgot.json()["reset_token"], "new_password": "NewVerifyPass1"},
    )
    assert reset.status_code == 200

    old_login = client.post("/api/v1/auth/login", json={"email": "verify@example.com", "password": "VerifyPass1"})
    assert old_login.status_code == 401

    new_login = client.post("/api/v1/auth/login", json={"email": "verify@example.com", "password": "NewVerifyPass1"})
    assert new_login.status_code == 200


def test_refresh_token_admin_listing_filtering_sorting_and_revoke(client: TestClient, db: Session) -> None:
    headers = admin_headers(client, db)
    login = client.post("/api/v1/auth/login", json={"email": "admin@example.com", "password": "AdminPass1"})
    assert login.status_code == 200

    active = client.get(
        "/api/v1/refresh-tokens?search=admin&status=active&sort=expires_at&direction=desc&page=1&page_size=10",
        headers=headers,
    )
    assert active.status_code == 200
    assert active.json()["total"] >= 1
    token_uuid = active.json()["items"][0]["uuid"]

    detail = client.get(f"/api/v1/refresh-tokens/{token_uuid}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["user_email"] == "admin@example.com"

    revoked = client.post(f"/api/v1/refresh-tokens/{token_uuid}/revoke", headers=headers)
    assert revoked.status_code == 200
    assert revoked.json()["is_active"] is False

    revoked_list = client.get("/api/v1/refresh-tokens?status=revoked", headers=headers)
    assert revoked_list.status_code == 200
    assert revoked_list.json()["total"] >= 1
