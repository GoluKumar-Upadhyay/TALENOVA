from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy import select
from app.api.v1.auth.router import router as auth_router
from app.api.v1.permissions.router import router as permission_router
from app.api.v1.refresh_tokens.router import router as refresh_token_router
from app.api.v1.roles.router import router as role_router
from app.api.v1.users.router import router as user_router
from app.api.v1.cms.router import router as cms_router
from app.api.v1.hero.router import router as hero_router
from app.api.v1.content.router import router as content_router
from app.api.v1.course_categories.router import router as course_category_router
from app.api.v1.courses.router import router as course_router
from app.api.v1.teachers.router import router as teacher_router
from app.api.v1.founders.router import router as founder_router
from app.api.v1.partners.router import router as partner_router
from app.api.v1.gallery.router import router as gallery_router
from app.api.v1.videos.router import router as video_router
from app.api.v1.projects.router import router as project_router
from app.api.v1.achievements.router import router as achievement_router
from app.api.v1.testimonials.router import router as testimonial_router
from app.api.v1.success_stories.router import router as success_story_router
from app.api.v1.internships.router import router as internship_router
from app.api.v1.events.router import router as event_router
from app.api.v1.contact.router import router as contact_router
from app.api.v1.faqs.router import router as faq_router
from app.api.v1.settings.router import router as settings_router
from app.api.v1.navigation.router import router as navigation_router
from app.api.v1.footer.router import router as footer_router
from app.api.v1.seo.router import router as seo_router
from app.api.v1.analytics.router import router as analytics_router
from app.api.v1.storage.router import router as storage_router
from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models.auth import Permission, Role, User
from app.services.user import passwords
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging
from app.middleware.security import RequestContextMiddleware, SecurityHeadersMiddleware

@asynccontextmanager
async def lifespan(application: FastAPI):
    """Initialize required application resources for the process lifetime."""
    import logging
    _log = logging.getLogger("talenova.startup")

    # ── PostgreSQL connectivity check ────────────────────────────────────────
    try:
        with SessionLocal() as db:
            from sqlalchemy import text
            db.execute(text("SELECT 1"))
            _log.info("PostgreSQL connect OK  ✓  (%s)", get_settings().database_url.split("@")[-1])

            # ── Admin seed ──────────────────────────────────────────────────
            if not db.scalar(select(User).where(User.email == str(get_settings().admin_email))):
                role = Role(name="admin", description="Full platform administrator")
                role.permissions = [
                    Permission(code=code, name=code.replace(":", " ").title())
                    for code in ("cms:read", "cms:write", "users:manage")
                ]
                db.add(
                    User(
                        email=str(get_settings().admin_email).lower(),
                        password_hash=passwords.hash(get_settings().admin_password),
                        is_email_verified=True,
                        email_verified_at=datetime.utcnow(),
                        roles=[role],
                    )
                )
                db.commit()
                _log.info("Admin user seeded  ✓")
    except Exception as exc:
        _log.error("PostgreSQL connect FAIL  ✗  %s", exc)

    # ── Supabase connectivity check ──────────────────────────────────────────
    try:
        from supabase import create_client
        settings = get_settings()
        _client = create_client(settings.supabase_url, settings.supabase_service_role_key)
        # List root of bucket — lightweight probe that confirms credentials work
        _client.storage.from_(settings.supabase_bucket).list("", {"limit": 1})
        _log.info("Supabase connect OK  ✓  bucket=%s", settings.supabase_bucket)
    except Exception as exc:
        _log.warning("Supabase connect FAIL  ✗  %s", exc)

    yield


app = FastAPI(title="TALENOVA API", version="0.1.0", lifespan=lifespan)
configure_logging()
register_exception_handlers(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
app.add_middleware(GZipMiddleware, minimum_size=1024)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[host.strip() for host in get_settings().allowed_hosts.split(",")],
)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestContextMiddleware)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(role_router, prefix="/api/v1")
app.include_router(permission_router, prefix="/api/v1")
app.include_router(refresh_token_router, prefix="/api/v1")
app.include_router(cms_router, prefix="/api/v1")
app.include_router(hero_router, prefix="/api/v1")
app.include_router(content_router, prefix="/api/v1")
app.include_router(course_category_router, prefix="/api/v1")
app.include_router(course_router, prefix="/api/v1")
app.include_router(teacher_router, prefix="/api/v1")
app.include_router(founder_router, prefix="/api/v1")
app.include_router(partner_router, prefix="/api/v1")
app.include_router(gallery_router, prefix="/api/v1")
app.include_router(video_router, prefix="/api/v1")
app.include_router(project_router, prefix="/api/v1")
app.include_router(achievement_router, prefix="/api/v1")
app.include_router(testimonial_router, prefix="/api/v1")
app.include_router(success_story_router, prefix="/api/v1")
app.include_router(internship_router, prefix="/api/v1")
app.include_router(event_router, prefix="/api/v1")
app.include_router(contact_router, prefix="/api/v1")
app.include_router(faq_router, prefix="/api/v1")
app.include_router(settings_router, prefix="/api/v1")
app.include_router(navigation_router, prefix="/api/v1")
app.include_router(footer_router, prefix="/api/v1")
app.include_router(seo_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(storage_router, prefix="/api/v1")
@app.get("/health", tags=["platform"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "talenova-api"}
