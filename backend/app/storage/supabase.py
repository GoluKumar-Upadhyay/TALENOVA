"""Supabase Storage operations for TALENOVA media management."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import PurePosixPath
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from supabase import Client, create_client

from app.core.config import get_settings


class SupabaseStorageService:
    """Validate, upload, list, replace, sign, and delete media assets."""

    roots = ("images", "videos", "documents")
    image_types = {"image/jpeg", "image/png", "image/webp", "image/gif"}
    video_types = {"video/mp4", "video/webm", "video/quicktime"}
    document_types = {
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
    }
    max_bytes = {
        "images": 10 * 1024 * 1024,
        "videos": 250 * 1024 * 1024,
        "documents": 50 * 1024 * 1024,
    }

    def __init__(self, client: Client | None = None, bucket: str | None = None) -> None:
        settings = get_settings()
        self.bucket = bucket or settings.supabase_bucket
        self.client: Client = client or create_client(settings.supabase_url, settings.supabase_service_role_key)

    async def upload_gallery_image(self, upload: UploadFile) -> str:
        """Validate and upload an image into the gallery folder."""

        item = await self.upload_image(upload, folder="images/gallery")
        return item["url"]

    async def upload(self, upload: UploadFile, folder: str = "images") -> dict:
        """Upload any supported media asset to the selected storage folder."""

        normalized_folder = self._normalize_folder(folder)
        root = self._root_for(normalized_folder)
        await self._validate_upload(upload, root)
        return await self._store(upload, normalized_folder, upsert=False)

    async def upload_image(self, upload: UploadFile, folder: str = "images") -> dict:
        """Upload an image asset."""

        normalized_folder = self._normalize_folder(folder)
        if self._root_for(normalized_folder) != "images":
            raise HTTPException(status_code=422, detail="Image uploads must target the images folder")
        await self._validate_upload(upload, "images")
        return await self._store(upload, normalized_folder, upsert=False)

    async def upload_video(self, upload: UploadFile, folder: str = "videos") -> dict:
        """Upload a video asset."""

        normalized_folder = self._normalize_folder(folder)
        if self._root_for(normalized_folder) != "videos":
            raise HTTPException(status_code=422, detail="Video uploads must target the videos folder")
        await self._validate_upload(upload, "videos")
        return await self._store(upload, normalized_folder, upsert=False)

    async def upload_document(self, upload: UploadFile, folder: str = "documents") -> dict:
        """Upload a document asset."""

        normalized_folder = self._normalize_folder(folder)
        if self._root_for(normalized_folder) != "documents":
            raise HTTPException(status_code=422, detail="Document uploads must target the documents folder")
        await self._validate_upload(upload, "documents")
        return await self._store(upload, normalized_folder, upsert=False)

    async def replace(self, file_id: str, upload: UploadFile) -> dict:
        """Replace an existing media object at the same storage path."""

        path = self._normalize_path(file_id)
        root = self._root_for(path)
        await self._validate_upload(upload, root)
        data = await upload.read()
        if not data:
            raise HTTPException(status_code=413, detail="Uploaded file is empty")
        if len(data) > self.max_bytes[root]:
            raise HTTPException(status_code=413, detail=f"{root.title()} uploads exceed the maximum allowed size")
        self._bucket().upload(path, data, {"content-type": upload.content_type, "upsert": "true"})
        return self._file_payload(path, upload.filename or PurePosixPath(path).name, upload.content_type or "", len(data), None)

    def list(
        self,
        folder: str | None = "images",
        search: str | None = None,
        media_type: str | None = None,
        sort: str = "name",
        direction: str = "asc",
        page: int = 1,
        page_size: int = 24,
    ) -> tuple[list[dict], int]:
        """List media objects for the media manager."""

        self._validate_list_options(sort, direction, media_type)
        folders = self.roots if folder in (None, "all") else (self._normalize_folder(folder),)
        items: list[dict] = []
        for current_folder in folders:
            items.extend(self._list_folder(current_folder, search, media_type))
        reverse = direction == "desc"
        if sort == "updated_at":
            items.sort(key=lambda item: item["updated_at"] or datetime.min, reverse=reverse)
        elif sort == "size":
            items.sort(key=lambda item: item["size"], reverse=reverse)
        else:
            items.sort(key=lambda item: item["name"].lower(), reverse=reverse)
        total = len(items)
        start = (page - 1) * page_size
        return items[start : start + page_size], total

    def signed_url(self, file_id: str, expires_in: int = 3600) -> dict:
        """Create a temporary signed URL for a stored object."""

        if expires_in < 1 or expires_in > 604800:
            raise HTTPException(status_code=422, detail="Signed URL expiry must be between 1 and 604800 seconds")
        path = self._normalize_path(file_id)
        response = self._bucket().create_signed_url(path, expires_in)
        signed_url = response.get("signedURL") or response.get("signed_url") or response.get("signedUrl")
        if not signed_url:
            raise HTTPException(status_code=502, detail="Supabase did not return a signed URL")
        return {"id": path, "signed_url": signed_url, "expires_in": expires_in}

    def delete(self, file_id: str) -> None:
        """Delete a media object after validating its folder boundary."""

        path = self._normalize_path(file_id)
        response = self._bucket().remove([path])
        if isinstance(response, dict) and response.get("error"):
            raise HTTPException(status_code=502, detail="Supabase failed to delete the file")

    def statistics(self) -> dict:
        """Return aggregate counts and byte sizes by storage root."""

        folders = []
        total_files = 0
        total_bytes = 0
        for root in self.roots:
            items = self._list_folder(root, None, None)
            byte_count = sum(item["size"] for item in items)
            folders.append({"folder": root, "files": len(items), "bytes": byte_count})
            total_files += len(items)
            total_bytes += byte_count
        return {"total_files": total_files, "total_bytes": total_bytes, "folders": folders}

    async def _store(self, upload: UploadFile, folder: str, upsert: bool) -> dict:
        data = await upload.read()
        if not data:
            raise HTTPException(status_code=413, detail="Uploaded file is empty")
        root = self._root_for(folder)
        if len(data) > self.max_bytes[root]:
            raise HTTPException(status_code=413, detail=f"{root.title()} uploads exceed the maximum allowed size")
        filename = self._safe_filename(upload.filename or "asset")
        suffix = PurePosixPath(filename).suffix.lower()
        stem = PurePosixPath(filename).stem[:80] or "asset"
        path = f"{folder}/{uuid4()}-{stem}{suffix}"
        self._bucket().upload(path, data, {"content-type": upload.content_type, "upsert": "true" if upsert else "false"})
        return self._file_payload(path, filename, upload.content_type or "", len(data), None)

    async def _validate_upload(self, upload: UploadFile, root: str) -> None:
        content_type = upload.content_type or "application/octet-stream"
        allowed = {
            "images": self.image_types,
            "videos": self.video_types,
            "documents": self.document_types,
        }[root]
        if content_type not in allowed:
            raise HTTPException(status_code=415, detail=f"Unsupported {root[:-1] if root.endswith('s') else root} media type")

    def _list_folder(self, folder: str, search: str | None, media_type: str | None) -> list[dict]:
        files = self._bucket().list(folder, {"limit": 1000, "sortBy": {"column": "name", "order": "asc"}})
        result = []
        for item in files or []:
            name = item.get("name", "")
            if not name or "/" in name:
                continue
            metadata = item.get("metadata") or {}
            if not metadata and not PurePosixPath(name).suffix:
                result.extend(self._list_folder(f"{folder}/{name}", search, media_type))
                continue
            content_type = metadata.get("mimetype") or metadata.get("contentType") or "application/octet-stream"
            if media_type and not content_type.startswith(f"{media_type}/"):
                continue
            if search and search.lower() not in name.lower():
                continue
            path = f"{folder}/{name}"
            result.append(
                self._file_payload(
                    path,
                    name,
                    content_type,
                    int(metadata.get("size") or item.get("size") or 0),
                    self._parse_datetime(item.get("updated_at") or item.get("created_at") or item.get("last_accessed_at")),
                )
            )
        return result

    def _file_payload(
        self,
        path: str,
        name: str,
        content_type: str,
        size: int,
        updated_at: datetime | None,
    ) -> dict:
        return {
            "id": path,
            "name": name,
            "folder": str(PurePosixPath(path).parent),
            "type": content_type,
            "url": self._bucket().get_public_url(path),
            "size": size,
            "updated_at": updated_at,
        }

    def _bucket(self):
        return self.client.storage.from_(self.bucket)

    def _normalize_folder(self, folder: str) -> str:
        path = self._clean_posix(folder)
        if path == "." or not path:
            raise HTTPException(status_code=422, detail="Storage folder is required")
        root = self._root_for(path)
        if root not in self.roots:
            raise HTTPException(status_code=422, detail="Unsupported storage folder")
        return path

    def _normalize_path(self, file_id: str) -> str:
        path = self._clean_posix(file_id)
        if PurePosixPath(path).name == "" or len(PurePosixPath(path).parts) < 2:
            raise HTTPException(status_code=422, detail="Storage file path is required")
        root = self._root_for(path)
        if root not in self.roots:
            raise HTTPException(status_code=422, detail="Invalid storage path")
        return path

    def _clean_posix(self, value: str) -> str:
        raw = (value or "").replace("\\", "/").strip("/")
        path = PurePosixPath(raw)
        if not raw or any(part in {"", ".", ".."} for part in path.parts):
            raise HTTPException(status_code=422, detail="Storage paths cannot contain relative segments")
        return str(path)

    def _root_for(self, value: str) -> str:
        return PurePosixPath(value).parts[0]

    def _safe_filename(self, filename: str) -> str:
        name = PurePosixPath(filename.replace("\\", "/")).name
        cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip(".-")
        return cleaned or "asset"

    def _validate_list_options(self, sort: str, direction: str, media_type: str | None) -> None:
        if sort not in {"name", "size", "updated_at"}:
            raise HTTPException(status_code=422, detail="Unsupported storage sort field")
        if direction not in {"asc", "desc"}:
            raise HTTPException(status_code=422, detail="Unsupported storage sort direction")
        if media_type not in {None, "image", "video", "application", "text"}:
            raise HTTPException(status_code=422, detail="Unsupported media type filter")

    def _parse_datetime(self, value: str | None) -> datetime | None:
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
