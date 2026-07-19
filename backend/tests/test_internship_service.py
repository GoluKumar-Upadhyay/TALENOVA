"""Internship validation tests."""
import pytest
from pydantic import ValidationError
from app.schemas.internship import InternshipWrite
def test_internship_type_is_constrained() -> None:
    """Only supported delivery formats are accepted."""
    with pytest.raises(ValidationError): InternshipWrite(title="AI", internship_type="invalid")
