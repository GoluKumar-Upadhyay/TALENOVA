"""FAQ API contracts."""
from app.schemas.faq import FAQWrite
def test_featured_seo_faq_is_supported() -> None:
    """FAQ payload includes featured and SEO fields."""
    item = FAQWrite(question="How does it work?", answer="With guidance", seo_slug="how", is_featured=True)
    assert item.is_featured and item.seo_slug == "how"
