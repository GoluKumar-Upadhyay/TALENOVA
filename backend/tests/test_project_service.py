"""Project service unit tests."""
from app.services.project import ProjectService
def test_project_value_lists_are_deduplicated() -> None:
    """Tags and technologies should be normalized before persistence."""
    values = {"technologies": ["Python", "Python"], "tags": ["AI", "AI"], "screenshot_urls": ["https://x", "https://x"]}
    result = ProjectService._normalize(values)
    assert result["technologies"] == ["Python"]
    assert result["tags"] == ["AI"]
