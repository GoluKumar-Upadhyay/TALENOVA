"""Authentication and account lifecycle REST API routes."""

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.schemas.auth import (
    AuthMessage,
    EmailVerificationRequest,
    EmailVerificationResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    ResetPasswordRequest,
    TokenPair,
    VerifyEmailRequest,
)
from app.schemas.user import UserRead
from app.services.auth import AuthService, token_hash
from app.services.user import passwords

router = APIRouter(prefix="/auth", tags=["auth"])
bearer = HTTPBearer()


def authenticated(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    """Validate a bearer access token and return its claims."""

    try:
        return jwt.decode(credentials.credentials, get_settings().jwt_secret, algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired access token") from exc


def require(permission: str):
    """FastAPI dependency factory enforcing a single permission code."""

    def dependency(claims: dict = Depends(authenticated)) -> dict:
        if permission not in claims.get("permissions", []):
            raise HTTPException(status_code=403, detail="Insufficient permission")
        return claims

    return dependency


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenPair:
    """Authenticate a user and issue access and refresh tokens."""

    return AuthService(db).login(str(payload.email), payload.password)


@router.post("/refresh", response_model=TokenPair)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)) -> TokenPair:
    """Rotate a valid refresh token and issue a new token pair."""

    return AuthService(db).refresh(payload.refresh_token)


@router.post("/logout", response_model=AuthMessage)
def logout(payload: LogoutRequest, db: Session = Depends(get_db)) -> AuthMessage:
    """Revoke a refresh token."""

    AuthService(db).logout(payload.refresh_token)
    return AuthMessage()


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)) -> ForgotPasswordResponse:
    """Create a one-time password reset token."""

    token, minutes = AuthService(db).forgot_password(str(payload.email))
    return ForgotPasswordResponse(reset_token=token, expires_in_minutes=minutes)


@router.post("/reset-password", response_model=AuthMessage)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)) -> AuthMessage:
    """Use a valid reset token to replace the account password."""

    AuthService(db).reset_password(payload.token, payload.new_password)
    return AuthMessage()


@router.post("/email-verification", response_model=EmailVerificationResponse)
def request_email_verification(
    payload: EmailVerificationRequest,
    db: Session = Depends(get_db),
) -> EmailVerificationResponse:
    """Create a one-time email verification token."""

    token, hours = AuthService(db).request_email_verification(str(payload.email))
    return EmailVerificationResponse(verification_token=token, expires_in_hours=hours)


@router.post("/verify-email", response_model=AuthMessage)
def verify_email(payload: VerifyEmailRequest, db: Session = Depends(get_db)) -> AuthMessage:
    """Mark a user's email as verified using a one-time token."""

    AuthService(db).verify_email(payload.token)
    return AuthMessage()


@router.get("/me", response_model=UserRead)
def me(claims: dict = Depends(authenticated), db: Session = Depends(get_db)) -> UserRead:
    """Return the authenticated user profile."""

    return AuthService(db).current_user(claims["sub"])
