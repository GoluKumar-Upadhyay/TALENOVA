"""Internship API contract tests."""
from app.schemas.internship import InternshipWrite
def test_internship_featured_and_stipend_fields() -> None:
    """CMS payload retains featured and stipend values."""
    item = InternshipWrite(title="AI Internship", stipend="₹20,000", is_featured=True)
    assert item.stipend == "₹20,000" and item.is_featured
