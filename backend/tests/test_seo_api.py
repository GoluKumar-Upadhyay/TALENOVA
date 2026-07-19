"""SEO API contract tests."""
from app.schemas.seo import SEOWrite
def test_seo_supports_hreflang() -> None:
    """Localized alternates are accepted."""
    assert SEOWrite(page_key="home", meta_title="Talenova", hreflang={"en": "/"}).hreflang["en"] == "/"
