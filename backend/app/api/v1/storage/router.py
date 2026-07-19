"""Storage and media-manager REST API routes."""

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile

from app.api.v1.auth.router import require
from app.schemas.storage import (
    StorageDeleteRead,
    StorageFilePage,
    StorageFileRead,
    StorageSignedUrlRead,
    StorageStatisticsRead,
)
from app.storage.supabase import SupabaseStorageService

router = APIRouter(prefix="/storage", tags=["storage"])


def get_storage_service() -> SupabaseStorageService:
    """Return the configured Supabase storage service."""

    return SupabaseStorageService()


@router.post(
    "/upload",
    response_model=StorageFileRead,
    dependencies=[Depends(require("cms:write"))],
    summary="Generic Upload API",
)
async def upload_file(
    file: UploadFile = File(...),
    folder: str = Form("images"),
    service: SupabaseStorageService = Depends(get_storage_service),
) -> StorageFileRead:
    """Upload any supported image, video, or document to a validated folder."""

    return await service.upload(file, folder)


@router.post(
    "/images",
    response_model=StorageFileRead,
    dependencies=[Depends(require("cms:write"))],
    summary="Image Upload",
)
async def upload_image(
    file: UploadFile = File(...),
    folder: str = Form("images"),
    service: SupabaseStorageService = Depends(get_storage_service),
) -> StorageFileRead:
    """Upload an image file to the images folder or an images subfolder."""

    return await service.upload_image(file, folder)


@router.post(
    "/videos",
    response_model=StorageFileRead,
    dependencies=[Depends(require("cms:write"))],
    summary="Video Upload",
)
async def upload_video(
    file: UploadFile = File(...),
    folder: str = Form("videos"),
    service: SupabaseStorageService = Depends(get_storage_service),
) -> StorageFileRead:
    """Upload a video file to the videos folder or a videos subfolder."""

    return await service.upload_video(file, folder)


@router.post(
    "/documents",
    response_model=StorageFileRead,
    dependencies=[Depends(require("cms:write"))],
    summary="Document Upload",
)
async def upload_document(
    file: UploadFile = File(...),
    folder: str = Form("documents"),
    service: SupabaseStorageService = Depends(get_storage_service),
) -> StorageFileRead:
    """Upload a document to the documents folder or a documents subfolder."""

    return await service.upload_document(file, folder)


@router.get(
    "/files",
    response_model=StorageFilePage,
    dependencies=[Depends(require("cms:read"))],
    summary="Media Manager",
)
def list_files(
    folder: str | None = Query(default="all"),
    search: str | None = None,
    media_type: str | None = None,
    sort: str = Query(default="name"),
    direction: str = Query(default="asc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=24, ge=1, le=100),
    service: SupabaseStorageService = Depends(get_storage_service),
) -> StorageFilePage:
    """List media files with folder support, search, filters, sorting, and pagination."""

    items, total = service.list(folder, search, media_type, sort, direction, page, page_size)
    return StorageFilePage(items=items, total=total, page=page, page_size=page_size)


@router.get(
    "/statistics",
    response_model=StorageStatisticsRead,
    dependencies=[Depends(require("cms:read"))],
    summary="Storage Statistics",
)
def storage_statistics(
    service: SupabaseStorageService = Depends(get_storage_service),
) -> StorageStatisticsRead:
    """Return file counts and byte totals across managed storage folders."""

    return service.statistics()


@router.post(
    "/signed-url",
    response_model=StorageSignedUrlRead,
    dependencies=[Depends(require("cms:read"))],
    summary="Signed URL",
)
def create_signed_url(
    file_id: str = Form(...),
    expires_in: int = Form(default=3600, ge=1, le=604800),
    service: SupabaseStorageService = Depends(get_storage_service),
) -> StorageSignedUrlRead:
    """Create a temporary signed URL for a stored media object."""

    return service.signed_url(file_id, expires_in)


@router.put(
    "/files/{file_id:path}",
    response_model=StorageFileRead,
    dependencies=[Depends(require("cms:write"))],
    summary="Replace",
)
async def replace_file(
    file_id: str,
    file: UploadFile = File(...),
    service: SupabaseStorageService = Depends(get_storage_service),
) -> StorageFileRead:
    """Replace an existing file at the same storage path."""

    return await service.replace(file_id, file)


@router.delete(
    "/files/{file_id:path}",
    response_model=StorageDeleteRead,
    dependencies=[Depends(require("cms:write"))],
    summary="Delete",
)
def delete_file(
    file_id: str,
    service: SupabaseStorageService = Depends(get_storage_service),
) -> StorageDeleteRead:
    """Remove a stored media object."""

    service.delete(file_id)
    return StorageDeleteRead(deleted=True, id=file_id)
