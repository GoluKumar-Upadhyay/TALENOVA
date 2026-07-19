"""Achievement schema contract tests."""
from app.schemas.achievement import AchievementWrite
def test_achievement_featured_flag_is_supported() -> None:
    """CMS may mark an achievement featured."""
    assert AchievementWrite(title="Patent", is_featured=True).is_featured is True
