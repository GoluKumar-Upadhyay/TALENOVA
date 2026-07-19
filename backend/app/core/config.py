from functools import lru_cache
from pathlib import Path
from pydantic import EmailStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[3] / ".env", extra="ignore")
    database_url: str
    jwt_secret: str
    admin_email: EmailStr
    admin_password: str
    environment: str = "development"
    allowed_hosts: str = "localhost,127.0.0.1,testserver"
    trusted_proxy_ips: str = ""
    enable_hsts: bool = False
    hsts_max_age: int = 31536000
    content_security_policy: str = (
        "default-src 'self'; base-uri 'self'; frame-ancestors 'none'; "
        "object-src 'none'; form-action 'self'"
    )
    supabase_url: str
    supabase_service_role_key: str
    supabase_bucket: str
    @field_validator("database_url")
    @classmethod
    def normalize_url(cls, value: str) -> str:
        return value.replace("postgresql://", "postgresql+psycopg://", 1) if value.startswith("postgresql://") else value

@lru_cache
def get_settings() -> Settings: return Settings()
