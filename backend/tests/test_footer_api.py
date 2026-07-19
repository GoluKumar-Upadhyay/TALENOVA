"""Footer API contract tests."""
from app.schemas.footer import FooterWrite
def test_footer_newsletter_configuration() -> None:
    """Newsletter configuration remains editable."""
    assert FooterWrite(newsletter_enabled=True).newsletter_enabled
