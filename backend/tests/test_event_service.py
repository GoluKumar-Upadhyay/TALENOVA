"""Event contract tests."""
from app.schemas.event import EventWrite
def test_event_mode_is_supported() -> None:
    """Events accept hybrid delivery."""
    assert EventWrite(title="Bootcamp", mode="hybrid").mode == "hybrid"
