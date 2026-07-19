"""FAQ schema tests."""
import pytest
from pydantic import ValidationError
from app.schemas.faq import FAQWrite
def test_faq_category_is_constrained() -> None:
    """Unsupported FAQ categories are rejected."""
    with pytest.raises(ValidationError): FAQWrite(question="Question?", answer="Answer", seo_slug="question", category="other")
