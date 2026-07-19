"""Unit tests for gallery validation rules."""

import pytest
from fastapi import HTTPException

from app.services.gallery import GalleryService


def test_gallery_rejects_non_https_urls() -> None:
    """Gallery media locations must not allow insecure URLs."""
    with pytest.raises(HTTPException) as raised:
        GalleryService._validate_storage_url("http://example.test/photo.jpg")
    assert raised.value.status_code == 422
