"""Navigation schema tests."""
from app.schemas.navigation import NavigationWrite
def test_navigation_supports_mobile_location() -> None:
    assert NavigationWrite(label="Home", href="/", location="mobile").location == "mobile"
