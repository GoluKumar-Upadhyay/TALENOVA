"""Website settings contract tests."""
from app.schemas.settings import SettingsWrite
def test_settings_support_maintenance_message() -> None:
    """Admin settings include a maintenance message."""
    assert SettingsWrite(site_name="Talenova", maintenance_message="Back soon").maintenance_message == "Back soon"
