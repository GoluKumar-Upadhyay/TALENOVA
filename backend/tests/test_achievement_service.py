"""Achievement service tests."""
from app.models.achievement import Achievement
def test_achievement_defaults_to_active() -> None:
    """New achievement records are active by default."""
    assert Achievement.__table__.c.is_active.default.arg is True
