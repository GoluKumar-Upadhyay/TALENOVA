"""Authentication, authorization, and account lifecycle operations."""

from datetime import datetime, timedelta
from hashlib import sha256
from secrets import token_urlsafe

import jwt
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.auth import User
from app.repositories.account_token import AccountTokenRepository
from app.repositories.refresh_token import RefreshTokenRepository
from app.repositories.user import UserRepository
from app.services.user import passwords


ACCESS_TOKEN_MINUTES = 15
REFRESH_TOKEN_DAYS = 14
PASSWORD_RESET_MINUTES = 30
EMAIL_VERIFICATION_HOURS = 24


def token_hash(value: str) -> str:
    """Hash opaque one-time and refresh tokens before persistence."""

    return sha256(value.encode()).hexdigest()


def permissions_for(user: User) -> list[str]:
    """Collect active permission codes from active user roles."""

    return sorted(
        {
            permission.code
            for role in user.roles
            if role.is_active and not role.is_deleted
            for permission in role.permissions
            if permission.is_active and not permission.is_deleted
        }
    )


class AuthService:
    """Coordinates login, JWTs, refresh, logout, reset, and verification flows."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.users = UserRepository(db)
        self.refresh_tokens = RefreshTokenRepository(db)
        self.account_tokens = AccountTokenRepository(db)

    def login(self, email: str, password: str):
        user = self.users.get_by_email(email.lower())
        if not user or not user.is_active or not passwords.verify(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        user.last_login_at = datetime.utcnow()
        self.db.commit()
        return self.issue(user)

    def issue(self, user: User):
        settings = get_settings()
        access = jwt.encode(
            {
                "sub": user.uuid,
                "user_id": user.id,
                "email": user.email,
                "permissions": permissions_for(user),
                "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_MINUTES),
            },
            settings.jwt_secret,
            algorithm="HS256",
        )
        refresh = token_urlsafe(48)
        self.refresh_tokens.create(
            {
                "user_id": user.id,
                "token_hash": token_hash(refresh),
                "expires_at": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_DAYS),
            }
        )
        from app.schemas.auth import TokenPair

        return TokenPair(access_token=access, refresh_token=refresh)

    def refresh(self, refresh_token: str):
        item = self.refresh_tokens.get_by_hash(token_hash(refresh_token))
        if not item or item.revoked_at or item.expires_at <= datetime.utcnow() or not item.user.is_active:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        self.refresh_tokens.revoke(item)
        return self.issue(item.user)

    def logout(self, refresh_token: str) -> None:
        item = self.refresh_tokens.get_by_hash(token_hash(refresh_token))
        if item and item.revoked_at is None:
            self.refresh_tokens.revoke(item)

    def forgot_password(self, email: str) -> tuple[str, int]:
        user = self.users.get_by_email(email.lower())
        if not user or not user.is_active:
            raise HTTPException(status_code=404, detail="User not found")
        token = token_urlsafe(48)
        self.account_tokens.create_password_reset(
            {
                "user_id": user.id,
                "token_hash": token_hash(token),
                "expires_at": datetime.utcnow() + timedelta(minutes=PASSWORD_RESET_MINUTES),
            }
        )
        return token, PASSWORD_RESET_MINUTES

    def reset_password(self, token: str, new_password: str) -> None:
        item = self.account_tokens.get_password_reset_by_hash(token_hash(token))
        if not item or item.used_at or item.expires_at <= datetime.utcnow():
            raise HTTPException(status_code=401, detail="Invalid or expired reset token")
        item.user.password_hash = passwords.hash(new_password)
        item.used_at = datetime.utcnow()
        self.refresh_tokens.revoke_for_user(item.user_id)
        self.db.commit()

    def request_email_verification(self, email: str) -> tuple[str, int]:
        user = self.users.get_by_email(email.lower())
        if not user or not user.is_active:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_email_verified:
            raise HTTPException(status_code=409, detail="Email is already verified")
        token = token_urlsafe(48)
        self.account_tokens.create_email_verification(
            {
                "user_id": user.id,
                "token_hash": token_hash(token),
                "expires_at": datetime.utcnow() + timedelta(hours=EMAIL_VERIFICATION_HOURS),
            }
        )
        return token, EMAIL_VERIFICATION_HOURS

    def verify_email(self, token: str) -> None:
        item = self.account_tokens.get_email_verification_by_hash(token_hash(token))
        if not item or item.used_at or item.expires_at <= datetime.utcnow():
            raise HTTPException(status_code=401, detail="Invalid or expired verification token")
        item.user.is_email_verified = True
        item.user.email_verified_at = datetime.utcnow()
        item.used_at = datetime.utcnow()
        self.db.commit()

    def current_user(self, user_uuid: str):
        user = self.users.get(user_uuid)
        if user is None or not user.is_active:
            raise HTTPException(status_code=401, detail="User not found")
        return user
