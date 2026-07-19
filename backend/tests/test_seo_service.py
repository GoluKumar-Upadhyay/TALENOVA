"""SEO validation tests."""
from app.schemas.seo import SEOWrite
def test_seo_supports_structured_data() -> None:
    """JSON-LD is accepted as a structured data object."""
    assert SEOWrite(page_key="home", meta_title="Talenova", structured_data={"@type": "Organization"}).structured_data["@type"] == "Organization"
