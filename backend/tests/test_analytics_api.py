"""Analytics API contract tests."""
from app.schemas.analytics import DateRange
def test_custom_date_range_is_supported() -> None:
    """Analytics accepts optional date boundaries."""
    assert DateRange(start="2026-01-01", end="2026-01-31").start is not None
