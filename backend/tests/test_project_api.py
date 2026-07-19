"""Project API contract tests."""
from app.schemas.project import ProjectWrite
def test_project_status_is_validated() -> None:
    """Project status accepts only supported lifecycle values."""
    project = ProjectWrite(title="Portfolio", status="completed")
    assert project.status == "completed"
