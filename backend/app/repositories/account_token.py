"""Database access implementation for password reset and verification tokens."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.auth import EmailVerificationToken, PasswordResetToken, User


class AccountTokenRepository:
    """Persists one-time account lifecycle tokens."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_password_reset(self, values: dict) -> PasswordResetToken:
        item = PasswordResetToken(**values)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_password_reset_by_hash(self, token_hash: str) -> PasswordResetToken | None:
        return self.db.scalar(
            select(PasswordResetToken)
            .options(selectinload(PasswordResetToken.user))
            .where(PasswordResetToken.token_hash == token_hash, PasswordResetToken.is_deleted.is_(False))
        )

    def create_email_verification(self, values: dict) -> EmailVerificationToken:
        item = EmailVerificationToken(**values)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_email_verification_by_hash(self, token_hash: str) -> EmailVerificationToken | None:
        return self.db.scalar(
            select(EmailVerificationToken)
            .options(selectinload(EmailVerificationToken.user))
            .where(EmailVerificationToken.token_hash == token_hash, EmailVerificationToken.is_deleted.is_(False))
        )

    def mark_used(self, item: PasswordResetToken | EmailVerificationToken, used_at) -> None:
        item.used_at = used_at
        self.db.commit()

    def save_user(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user
