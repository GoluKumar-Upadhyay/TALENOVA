"""Storage API and Supabase service coverage."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from io import BytesIO

import jwt
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from starlette.datastructures import UploadFile

from app.api.v1.storage.router import get_storage_service
from app.core.config import get_settings
from app.main import app
from app.storage.supabase import SupabaseStorageService


class FakeBucket:
    def __init__(self) -> None:
        self.objects: dict[str, dict] = {}

    def upload(self, path: str, data: bytes, options: dict) -> None:
        if options.get("upsert") == "false" and path in self.objects:
            raise AssertionError("duplicate upload without upsert")
        self.objects[path] = {
            "data": data,
            "content_type": options.get("content-type"),
            "updated_at": "2026-07-19T00:00:00Z",
        }

    def get_public_url(self, path: str) -> str:
        return f"https://storage.example.test/public/{path}"

    def list(self, folder: str, options: dict) -> list[dict]:
        prefix = f"{folder}/"
        files = []
        folders = set()
        for path, item in self.objects.items():
            if not path.startswith(prefix):
                continue
            name = path[len(prefix) :]
            if "/" in name:
                folders.add(name.split("/", 1)[0])
                continue
            files.append(
                {
                    "name": name,
                    "updated_at": item["updated_at"],
                    "metadata": {"mimetype": item["content_type"], "size": len(item["data"])},
                }
            )
        return [{"name": folder_name, "metadata": None} for folder_name in sorted(folders)] + files

    def remove(self, paths: list[str]) -> dict:
        for path in paths:
            self.objects.pop(path, None)
        return {}

    def create_signed_url(self, path: str, expires_in: int) -> dict:
        return {"signedURL": f"https://storage.example.test/signed/{path}?expires={expires_in}"}


class FakeStorageClient:
    def __init__(self, bucket: FakeBucket) -> None:
        self.bucket = bucket
        self.storage = self

    def from_(self, bucket: str) -> FakeBucket:
        return self.bucket


def upload_file(name: str, content_type: str, data: bytes = b"file-bytes") -> UploadFile:
    return UploadFile(filename=name, file=BytesIO(data), headers={"content-type": content_type})


def storage_service() -> tuple[SupabaseStorageService, FakeBucket]:
    bucket = FakeBucket()
    return SupabaseStorageService(client=FakeStorageClient(bucket), bucket="test"), bucket


def auth_headers(*permissions: str) -> dict[str, str]:
    token = jwt.encode(
        {
            "sub": "test-user",
            "permissions": list(permissions),
            "exp": datetime.now(tz=timezone.utc).timestamp() + 900,
        },
        get_settings().jwt_secret,
        algorithm="HS256",
    )
    return {"Authorization": f"Bearer {token}"}


def test_storage_service_uploads_lists_replaces_signs_deletes_and_counts() -> None:
    service, bucket = storage_service()

    image = asyncio.run(service.upload_image(upload_file("Hero Image.png", "image/png"), "images/home"))
    assert image["id"].startswith("images/home/")
    assert image["name"] == "Hero-Image.png"
    assert bucket.objects[image["id"]]["content_type"] == "image/png"

    video = asyncio.run(service.upload_video(upload_file("lesson.mp4", "video/mp4", b"video"), "videos/classes"))
    document = asyncio.run(service.upload_document(upload_file("brochure.pdf", "application/pdf", b"pdf"), "documents"))
    generic = asyncio.run(service.upload(upload_file("notes.txt", "text/plain", b"text"), "documents/notes"))

    page, total = service.list(folder="all", search=None, media_type=None, sort="size", direction="desc", page=1, page_size=10)
    assert total == 4
    assert {item["id"] for item in page} == {image["id"], video["id"], document["id"], generic["id"]}

    filtered, filtered_total = service.list(
        folder="documents",
        search="brochure",
        media_type="application",
        sort="name",
        direction="asc",
        page=1,
        page_size=10,
    )
    assert filtered_total == 1
    assert filtered[0]["id"] == document["id"]

    replaced = asyncio.run(service.replace(image["id"], upload_file("replacement.png", "image/png", b"new-image")))
    assert replaced["id"] == image["id"]
    assert bucket.objects[image["id"]]["data"] == b"new-image"

    signed = service.signed_url(image["id"], 120)
    assert signed["signed_url"].endswith("?expires=120")

    stats = service.statistics()
    assert stats["total_files"] == 4
    assert {folder["folder"]: folder["files"] for folder in stats["folders"]} == {
        "images": 1,
        "videos": 1,
        "documents": 2,
    }

    service.delete(document["id"])
    assert document["id"] not in bucket.objects


def test_storage_service_rejects_invalid_folder_type_and_paths() -> None:
    service, _bucket = storage_service()

    with pytest.raises(HTTPException) as wrong_folder:
        asyncio.run(service.upload_image(upload_file("image.png", "image/png"), "documents"))
    assert wrong_folder.value.status_code == 422

    with pytest.raises(HTTPException) as wrong_type:
        asyncio.run(service.upload_video(upload_file("clip.txt", "text/plain"), "videos"))
    assert wrong_type.value.status_code == 415

    with pytest.raises(HTTPException) as traversal:
        asyncio.run(service.upload(upload_file("safe.pdf", "application/pdf"), "documents/../images"))
    assert traversal.value.status_code == 422

    with pytest.raises(HTTPException) as root_only:
        service.delete("images")
    assert root_only.value.status_code == 422


class FakeRouterStorage:
    async def upload(self, file, folder):
        return {"id": f"{folder}/asset.png", "name": file.filename, "folder": folder, "type": file.content_type, "url": "https://u", "size": 3}

    async def upload_image(self, file, folder):
        return await self.upload(file, folder)

    async def upload_video(self, file, folder):
        return {"id": f"{folder}/asset.mp4", "name": file.filename, "folder": folder, "type": file.content_type, "url": "https://v", "size": 3}

    async def upload_document(self, file, folder):
        return {"id": f"{folder}/asset.pdf", "name": file.filename, "folder": folder, "type": file.content_type, "url": "https://d", "size": 3}

    async def replace(self, file_id, file):
        return {"id": file_id, "name": file.filename, "folder": "images", "type": file.content_type, "url": "https://r", "size": 3}

    def list(self, folder, search, media_type, sort, direction, page, page_size):
        return (
            [{"id": "images/a.png", "name": "a.png", "folder": "images", "type": "image/png", "url": "https://u", "size": 3}],
            1,
        )

    def statistics(self):
        return {"total_files": 1, "total_bytes": 3, "folders": [{"folder": "images", "files": 1, "bytes": 3}]}

    def signed_url(self, file_id, expires_in):
        return {"id": file_id, "signed_url": "https://signed", "expires_in": expires_in}

    def delete(self, file_id):
        return None


def test_storage_router_endpoints_and_swagger_schema() -> None:
    app.dependency_overrides[get_storage_service] = lambda: FakeRouterStorage()
    client = TestClient(app)
    read_headers = auth_headers("cms:read")
    write_headers = auth_headers("cms:write", "cms:read")
    try:
        image = client.post(
            "/api/v1/storage/images",
            headers=write_headers,
            data={"folder": "images"},
            files={"file": ("a.png", b"abc", "image/png")},
        )
        assert image.status_code == 200
        assert image.json()["id"] == "images/asset.png"

        video = client.post(
            "/api/v1/storage/videos",
            headers=write_headers,
            data={"folder": "videos"},
            files={"file": ("a.mp4", b"abc", "video/mp4")},
        )
        assert video.status_code == 200

        document = client.post(
            "/api/v1/storage/documents",
            headers=write_headers,
            data={"folder": "documents"},
            files={"file": ("a.pdf", b"abc", "application/pdf")},
        )
        assert document.status_code == 200

        listed = client.get("/api/v1/storage/files?folder=all&page=1&page_size=10", headers=read_headers)
        assert listed.status_code == 200
        assert listed.json()["total"] == 1

        signed = client.post(
            "/api/v1/storage/signed-url",
            headers=read_headers,
            data={"file_id": "images/a.png", "expires_in": 60},
        )
        assert signed.status_code == 200
        assert signed.json()["signed_url"] == "https://signed"

        replaced = client.put(
            "/api/v1/storage/files/images/a.png",
            headers=write_headers,
            files={"file": ("b.png", b"abc", "image/png")},
        )
        assert replaced.status_code == 200
        assert replaced.json()["id"] == "images/a.png"

        stats = client.get("/api/v1/storage/statistics", headers=read_headers)
        assert stats.status_code == 200
        assert stats.json()["total_files"] == 1

        deleted = client.delete("/api/v1/storage/files/images/a.png", headers=write_headers)
        assert deleted.status_code == 200
        assert deleted.json() == {"deleted": True, "id": "images/a.png"}

        openapi = client.get("/openapi.json").json()
        operation_summaries = {
            operation["summary"]
            for path in openapi["paths"].values()
            for operation in path.values()
            if isinstance(operation, dict) and "summary" in operation
        }
        assert {
            "Generic Upload API",
            "Image Upload",
            "Video Upload",
            "Document Upload",
            "Media Manager",
            "Storage Statistics",
            "Signed URL",
            "Replace",
            "Delete",
        }.issubset(operation_summaries)
    finally:
        app.dependency_overrides.clear()
