"""Authentication and account recovery API contracts."""

from pydantic import BaseModel, EmailStr, Field, field_validator


def validate_password_strength(value: str) -> str:
    """Enforce the platform password policy in every password-bearing schema."""

    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if len(value) > 128:
        raise ValueError("Password must be at most 128 characters long")
    if not any(character.islower() for character in value):
        raise ValueError("Password must include a lowercase letter")
    if not any(character.isupper() for character in value):
        raise ValueError("Password must include an uppercase letter")
    if not any(character.isdigit() for character in value):
        raise ValueError("Password must include a number")
    return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=32, max_length=256)


class LogoutRequest(BaseModel):
    refresh_token: str = Field(min_length=32, max_length=256)


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    reset_token: str
    expires_in_minutes: int


class ResetPasswordRequest(BaseModel):
    token: str = Field(min_length=32, max_length=256)
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        return validate_password_strength(value)


class EmailVerificationRequest(BaseModel):
    email: EmailStr


class EmailVerificationResponse(BaseModel):
    verification_token: str
    expires_in_hours: int


class VerifyEmailRequest(BaseModel):
    token: str = Field(min_length=32, max_length=256)


class AuthMessage(BaseModel):
    ok: bool = True
