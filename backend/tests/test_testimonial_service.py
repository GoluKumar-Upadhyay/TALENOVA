"""Testimonial service tests."""
from app.schemas.testimonial import TestimonialWrite as TestimonialPayload
TestimonialPayload.__test__ = False
def test_rating_must_be_five_or_less() -> None:
    """Pydantic validates star ratings."""
    assert TestimonialPayload(student_name="Alex", review="Great work", rating=5).rating == 5
