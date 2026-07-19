"""LMS course service — business logic layer."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session


from app.repositories.course import CourseRepository


class CourseService:
    SORT_FIELDS = set(CourseRepository.SORT_FIELDS)

    def __init__(self, db: Session):
        self.repo = CourseRepository(db)

    # ── Courses ───────────────────────────────────────────────────────────────

    def list(self, search, category_id, mentor_id, published, coming_soon, is_active, sort, direction, page, page_size):
        if sort not in self.SORT_FIELDS:
            raise HTTPException(422, "Unsupported course sort field")
        if direction not in {"asc", "desc"}:
            raise HTTPException(422, "Unsupported sort direction")
        return self.repo.list(search, category_id, mentor_id, published, coming_soon, is_active, sort, direction, page, page_size)

    def get(self, uuid: str):
        item = self.repo.get(uuid)
        if not item:
            raise HTTPException(404, "Course not found")
        return item

    def get_by_slug(self, slug: str):
        item = self.repo.get_by_slug(slug)
        if not item:
            raise HTTPException(404, "Course not found")
        return item

    def create(self, data: dict):
        return self.repo.create(data)

    def update(self, uuid: str, data: dict):
        return self.repo.save(self.get(uuid), data)

    def delete(self, uuid: str):
        self.repo.save(self.get(uuid), {"is_deleted": True})

    # ── Modules ───────────────────────────────────────────────────────────────

    def list_modules(self, course_uuid: str):
        course = self.get(course_uuid)
        return self.repo.list_modules(course.id)

    def create_module(self, course_uuid: str, data: dict):
        course = self.get(course_uuid)
        return self.repo.create_module(course.id, data)

    def get_module(self, mod_uuid: str):
        mod = self.repo.get_module(mod_uuid)
        if not mod:
            raise HTTPException(404, "Module not found")
        return mod

    def update_module(self, mod_uuid: str, data: dict):
        return self.repo.save_module(self.get_module(mod_uuid), data)

    def delete_module(self, mod_uuid: str):
        self.repo.delete_module(self.get_module(mod_uuid))

    def reorder_modules(self, course_uuid: str, ordered_uuids: list[str]):
        course = self.get(course_uuid)
        return self.repo.reorder_modules(course.id, ordered_uuids)

    # ── Submodules ────────────────────────────────────────────────────────────

    def create_submodule(self, mod_uuid: str, data: dict):
        mod = self.get_module(mod_uuid)
        return self.repo.create_submodule(mod.id, data)

    def get_submodule(self, sub_uuid: str):
        sub = self.repo.get_submodule(sub_uuid)
        if not sub:
            raise HTTPException(404, "Submodule not found")
        return sub

    def update_submodule(self, sub_uuid: str, data: dict):
        return self.repo.save_submodule(self.get_submodule(sub_uuid), data)

    def delete_submodule(self, sub_uuid: str):
        self.repo.delete_submodule(self.get_submodule(sub_uuid))

    def reorder_submodules(self, mod_uuid: str, ordered_uuids: list[str]):
        mod = self.get_module(mod_uuid)
        return self.repo.reorder_submodules(mod.id, ordered_uuids)

    # ── Batches ───────────────────────────────────────────────────────────────

    def list_batches(self, course_uuid: str):
        course = self.get(course_uuid)
        return self.repo.list_batches(course.id)

    def create_batch(self, course_uuid: str, data: dict):
        course = self.get(course_uuid)
        return self.repo.create_batch(course.id, data)

    def get_batch(self, batch_uuid: str):
        b = self.repo.get_batch(batch_uuid)
        if not b:
            raise HTTPException(404, "Batch not found")
        return b

    def update_batch(self, batch_uuid: str, data: dict):
        return self.repo.save_batch(self.get_batch(batch_uuid), data)

    def delete_batch(self, batch_uuid: str):
        self.repo.delete_batch(self.get_batch(batch_uuid))

    # ── Applications ──────────────────────────────────────────────────────────

    def list_applications(self, course_uuid: str, search: str | None, status: str | None, page: int, page_size: int):
        course = self.get(course_uuid)
        return self.repo.list_applications(course.id, search, status, page, page_size)

    def submit_application(self, course_uuid: str, data: dict):
        course = self.get(course_uuid)
        # If batch_id provided, convert to int PK from batch uuid
        batch_uuid = data.pop("batch_uuid", None)
        if batch_uuid:
            b = self.repo.get_batch(batch_uuid)
            if b:
                data["batch_id"] = b.id
        return self.repo.create_application(course.id, data)

    def update_application(self, app_uuid: str, data: dict):
        app = self.repo.get_application(app_uuid)
        if not app:
            raise HTTPException(404, "Application not found")
        return self.repo.save_application(app, data)
