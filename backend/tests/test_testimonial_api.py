"""Testimonial API schema tests."""
from app.schemas.testimonial import TestimonialWrite as TestimonialPayload
TestimonialPayload.__test__ = False
def test_featured_testimonial_is_supported() -> None:
    """CMS can choose homepage testimonials."""
    assert TestimonialPayload(student_name="Alex", review="Great work", rating=5, is_featured=True).is_featured
