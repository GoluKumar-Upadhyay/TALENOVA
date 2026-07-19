"""Success story schema integration contracts."""
from app.schemas.success_story import SuccessStoryWrite
def test_success_story_accepts_company_logo_url() -> None:
    """Company logo URL is retained for public cards."""
    assert SuccessStoryWrite(name="Alex", story="A complete career transformation story", company_logo_url="https://storage/logo.png").company_logo_url
