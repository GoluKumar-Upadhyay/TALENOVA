"""Navigation validation tests."""
import pytest
from fastapi import HTTPException
from app.services.navigation import NavigationService
def test_external_link_requires_absolute_url() -> None:
    with pytest.raises(HTTPException): NavigationService._validate({"location":"header", "is_external":True, "href":"/relative"})
