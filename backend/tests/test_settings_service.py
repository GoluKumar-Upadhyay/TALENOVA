"""Website settings validation tests."""
import pytest
from pydantic import ValidationError
from app.schemas.settings import SettingsWrite
def test_only_light_theme_is_allowed() -> None:
    """Version one intentionally exposes a light theme only."""
    with pytest.raises(ValidationError): SettingsWrite(site_name="Talenova", default_theme="dark")
