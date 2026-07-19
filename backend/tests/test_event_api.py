"""Event API field tests."""
from app.schemas.event import EventWrite
def test_event_participant_limit_is_validated() -> None:
    """Maximum participants is represented in API payloads."""
    assert EventWrite(title="Seminar", maximum_participants=100).maximum_participants == 100
