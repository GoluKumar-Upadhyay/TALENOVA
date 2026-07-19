"""Storage API validation and representation contracts."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

StorageRoot = Literal["images", "videos", "documents"]


class StorageFileRead(BaseModel):
    id: str
    name: str
    folder: str
    type: str
    url: str
    size: int = 0
    updated_at: datetime | None = None


class StorageFilePage(BaseModel):
    items: list[StorageFileRead]
    total: int
    page: int
    page_size: int


class StorageSignedUrlRead(BaseModel):
    id: str
    signed_url: str
    expires_in: int = Field(ge=1, le=604800)


class StorageDeleteRead(BaseModel):
    deleted: bool
    id: str


class StorageFolderStats(BaseModel):
    folder: str
    files: int
    bytes: int


class StorageStatisticsRead(BaseModel):
    total_files: int
    total_bytes: int
    folders: list[StorageFolderStats]
