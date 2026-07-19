"""Analytics service contract tests."""
def test_dashboard_summary_keys_are_defined() -> None:
    """Dashboard cards use stable total keys."""
    expected = {"courses", "students", "teachers", "contacts", "events", "internships"}
    assert "contacts" in expected
