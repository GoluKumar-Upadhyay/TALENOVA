"""Success story service tests."""
from app.schemas.success_story import SuccessStoryWrite
def test_success_story_supports_featured_outcome() -> None:
    """Featured career outcomes are accepted."""
    assert SuccessStoryWrite(name="Alex", story="A complete career transformation story", is_featured=True).is_featured
