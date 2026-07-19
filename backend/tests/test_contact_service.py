"""Contact service tests."""
import pytest
from fastapi import HTTPException
from app.services.contact import ContactService
def test_college_requires_organization() -> None:
    """College inquiries must identify their institution."""
    with pytest.raises(HTTPException): ContactService(None).submit({"contact_type":"college"})
