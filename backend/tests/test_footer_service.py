"""Footer schema tests."""
from app.schemas.footer import FooterWrite
def test_footer_legal_links_are_supported() -> None:
    """Legal links can be edited with footer content."""
    value = FooterWrite(legal_links=[{"label": "Privacy Policy", "href": "/privacy"}])
    assert value.legal_links[0]["label"] == "Privacy Policy"
