"""Milestone 3 business module route and schema coverage."""

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.analytics import AnalyticsEventPage
from app.schemas.contact import ContactPage
from app.schemas.course import CoursePage
from app.schemas.footer import FooterPage
from app.schemas.founder import FounderPage
from app.schemas.gallery import GalleryCategoryPage, GalleryImagePage
from app.schemas.hero import HeroPage, StatisticPage
from app.schemas.navigation import NavigationPage
from app.schemas.partner import PartnerPage
from app.schemas.seo import SEOPage
from app.schemas.settings import SettingsPage
from app.schemas.teacher import TeacherPage
from app.schemas.video import VideoPage


def test_remaining_business_modules_are_registered_with_crud_routes() -> None:
    """OpenAPI exposes the completed route surface for all remaining modules."""

    openapi = TestClient(app).get("/openapi.json").json()
    paths = openapi["paths"]
    expected = {
        "/api/v1/courses": {"get", "post"},
        "/api/v1/courses/{uuid}": {"get", "put", "delete"},
        "/api/v1/teachers": {"get", "post"},
        "/api/v1/teachers/{uuid}": {"get", "put", "delete"},
        "/api/v1/founders": {"get", "post"},
        "/api/v1/founders/{uuid}": {"get", "delete"},
        "/api/v1/founders/id/{uuid}": {"put"},
        "/api/v1/partners": {"get", "post"},
        "/api/v1/partners/{uuid}": {"get", "put", "delete"},
        "/api/v1/gallery": {"get", "post"},
        "/api/v1/gallery/{uuid}": {"get", "put", "delete"},
        "/api/v1/gallery/categories": {"get", "post"},
        "/api/v1/gallery/categories/{uuid}": {"get", "put", "delete"},
        "/api/v1/videos": {"get", "post"},
        "/api/v1/videos/{uuid}": {"get", "put", "delete"},
        "/api/v1/contact": {"get", "post"},
        "/api/v1/contact/{uuid}": {"get", "put", "delete"},
        "/api/v1/hero": {"get", "post"},
        "/api/v1/hero/{uuid}": {"get", "put", "delete"},
        "/api/v1/hero/statistics": {"get", "post"},
        "/api/v1/hero/statistics/{uuid}": {"get", "put", "delete"},
        "/api/v1/content/{module}": {"get", "post"},
        "/api/v1/content/{module}/{uuid}": {"get"},
        "/api/v1/content/{uuid}": {"put", "delete"},
        "/api/v1/navigation": {"get", "post"},
        "/api/v1/navigation/{uuid}": {"get", "put", "delete"},
        "/api/v1/footer/all": {"get"},
        "/api/v1/footer": {"get", "post", "put"},
        "/api/v1/footer/{uuid}": {"get", "put", "delete"},
        "/api/v1/seo": {"get", "post", "put"},
        "/api/v1/seo/{uuid}": {"get", "put", "delete"},
        "/api/v1/settings/all": {"get"},
        "/api/v1/settings": {"get", "post", "put"},
        "/api/v1/settings/{uuid}": {"get", "put", "delete"},
        "/api/v1/analytics": {"get", "post"},
        "/api/v1/analytics/{uuid}": {"get", "put", "delete"},
        "/api/v1/analytics/dashboard": {"get"},
    }

    for path, methods in expected.items():
        assert path in paths
        assert methods.issubset(set(paths[path]))


def test_remaining_business_modules_have_page_response_contracts() -> None:
    """Paginated modules share the page envelope required by Milestone 3."""

    page_classes = [
        AnalyticsEventPage,
        ContactPage,
        CoursePage,
        FooterPage,
        FounderPage,
        GalleryCategoryPage,
        GalleryImagePage,
        HeroPage,
        NavigationPage,
        PartnerPage,
        SEOPage,
        SettingsPage,
        StatisticPage,
        TeacherPage,
        VideoPage,
    ]

    for page_class in page_classes:
        page = page_class(items=[], total=0, page=1, page_size=24)
        assert page.total == 0
        assert page.items == []
