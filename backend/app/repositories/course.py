"""LMS course repository — full CRUD for courses, modules, submodules, batches, applications."""

from __future__ import annotations

import re
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.course import (
    Course, CourseCurriculumItem,
    CourseModule, CourseSubmodule,
    CourseBatch, CourseApplication,
)


class CourseRepository:
    SORT_FIELDS = {
        "title": Course.title,
        "display_order": Course.display_order,
        "created_at": Course.created_at,
        "duration": Course.duration,
    }

    def __init__(self, db: Session):
        self.db = db

    # ── Course CRUD ───────────────────────────────────────────────────────────

    def _course_options(self):
        return [
            selectinload(Course.curriculum),
            selectinload(Course.modules).selectinload(CourseModule.submodules),
            selectinload(Course.batches),
        ]

    def list(self, search, category_id, mentor_id, published, coming_soon, is_active, sort, direction, page, size):
        q = [Course.is_deleted.is_(False)]
        if search:
            q.append(Course.title.ilike(f"%{search}%"))
        if category_id is not None:
            q.append(Course.category_id == category_id)
        if mentor_id is not None:
            q.append(Course.mentor_id == mentor_id)
        if published is not None:
            q.append(Course.is_published == published)
        if coming_soon is not None:
            q.append(Course.is_coming_soon == coming_soon)
        if is_active is not None:
            q.append(Course.is_active == is_active)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        stmt = select(Course).options(*self._course_options()).where(*q).order_by(order)
        items = list(self.db.scalars(stmt.offset((page - 1) * size).limit(size)))
        total = self.db.scalar(select(func.count()).select_from(Course).where(*q)) or 0
        return items, total

    def get(self, uuid: str) -> Course | None:
        return self.db.scalar(
            select(Course).options(*self._course_options())
            .where(Course.uuid == uuid, Course.is_deleted.is_(False))
        )

    def get_by_slug(self, slug: str) -> Course | None:
        return self.db.scalar(
            select(Course).options(*self._course_options())
            .where(Course.slug == slug, Course.is_deleted.is_(False))
        )

    def create(self, data: dict) -> Course:
        curriculum_data = data.pop("curriculum", [])
        if not data.get("slug") and data.get("title"):
            data["slug"] = self._unique_slug(data["title"])
        item = Course(**data)
        item.curriculum = [CourseCurriculumItem(**c) for c in curriculum_data]
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return self.get(item.uuid) or item

    def save(self, item: Course, data: dict) -> Course:
        curriculum_data = data.pop("curriculum", None)
        for k, v in data.items():
            setattr(item, k, v)
        if curriculum_data is not None:
            for c in list(item.curriculum):
                self.db.delete(c)
            item.curriculum = [CourseCurriculumItem(**c) for c in curriculum_data]
        self.db.commit()
        self.db.refresh(item)
        return self.get(item.uuid) or item

    # ── Module CRUD ───────────────────────────────────────────────────────────

    def list_modules(self, course_id: int) -> list[CourseModule]:
        return list(self.db.scalars(
            select(CourseModule)
            .options(selectinload(CourseModule.submodules))
            .where(CourseModule.course_id == course_id)
            .order_by(CourseModule.position)
        ))

    def get_module(self, uuid: str) -> CourseModule | None:
        return self.db.scalar(
            select(CourseModule).options(selectinload(CourseModule.submodules))
            .where(CourseModule.uuid == uuid)
        )

    def create_module(self, course_id: int, data: dict) -> CourseModule:
        submodule_data = data.pop("submodules", [])
        # Auto-position at end
        if "position" not in data or data["position"] == 0:
            count = self.db.scalar(
                select(func.count()).select_from(CourseModule).where(CourseModule.course_id == course_id)
            ) or 0
            data["position"] = count
        mod = CourseModule(course_id=course_id, **data)
        mod.submodules = [CourseSubmodule(module_id=0, **s) for s in submodule_data]
        self.db.add(mod)
        self.db.commit()
        self.db.refresh(mod)
        # Fix submodule module_id
        for s in mod.submodules:
            s.module_id = mod.id
        self.db.commit()
        return self.get_module(mod.uuid) or mod

    def save_module(self, mod: CourseModule, data: dict) -> CourseModule:
        data.pop("submodules", None)  # submodules managed separately
        for k, v in data.items():
            setattr(mod, k, v)
        self.db.commit()
        self.db.refresh(mod)
        return self.get_module(mod.uuid) or mod

    def delete_module(self, mod: CourseModule) -> None:
        self.db.delete(mod)
        self.db.commit()

    def reorder_modules(self, course_id: int, ordered_uuids: list[str]) -> list[CourseModule]:
        for pos, uuid in enumerate(ordered_uuids):
            mod = self.db.scalar(select(CourseModule).where(CourseModule.uuid == uuid, CourseModule.course_id == course_id))
            if mod:
                mod.position = pos
        self.db.commit()
        return self.list_modules(course_id)

    # ── Submodule CRUD ────────────────────────────────────────────────────────

    def get_submodule(self, uuid: str) -> CourseSubmodule | None:
        return self.db.scalar(select(CourseSubmodule).where(CourseSubmodule.uuid == uuid))

    def create_submodule(self, module_id: int, data: dict) -> CourseSubmodule:
        if "position" not in data or data["position"] == 0:
            count = self.db.scalar(
                select(func.count()).select_from(CourseSubmodule).where(CourseSubmodule.module_id == module_id)
            ) or 0
            data["position"] = count
        sub = CourseSubmodule(module_id=module_id, **data)
        self.db.add(sub)
        self.db.commit()
        self.db.refresh(sub)
        return sub

    def save_submodule(self, sub: CourseSubmodule, data: dict) -> CourseSubmodule:
        for k, v in data.items():
            setattr(sub, k, v)
        self.db.commit()
        self.db.refresh(sub)
        return sub

    def delete_submodule(self, sub: CourseSubmodule) -> None:
        self.db.delete(sub)
        self.db.commit()

    def reorder_submodules(self, module_id: int, ordered_uuids: list[str]) -> list[CourseSubmodule]:
        for pos, uuid in enumerate(ordered_uuids):
            sub = self.db.scalar(select(CourseSubmodule).where(CourseSubmodule.uuid == uuid, CourseSubmodule.module_id == module_id))
            if sub:
                sub.position = pos
        self.db.commit()
        return list(self.db.scalars(
            select(CourseSubmodule).where(CourseSubmodule.module_id == module_id).order_by(CourseSubmodule.position)
        ))

    # ── Batch CRUD ────────────────────────────────────────────────────────────

    def list_batches(self, course_id: int) -> list[CourseBatch]:
        return list(self.db.scalars(
            select(CourseBatch).where(CourseBatch.course_id == course_id).order_by(CourseBatch.start_date)
        ))

    def get_batch(self, uuid: str) -> CourseBatch | None:
        return self.db.scalar(select(CourseBatch).where(CourseBatch.uuid == uuid))

    def create_batch(self, course_id: int, data: dict) -> CourseBatch:
        batch = CourseBatch(course_id=course_id, **data)
        self.db.add(batch)
        self.db.commit()
        self.db.refresh(batch)
        return batch

    def save_batch(self, batch: CourseBatch, data: dict) -> CourseBatch:
        for k, v in data.items():
            setattr(batch, k, v)
        self.db.commit()
        self.db.refresh(batch)
        return batch

    def delete_batch(self, batch: CourseBatch) -> None:
        self.db.delete(batch)
        self.db.commit()

    # ── Application CRUD ──────────────────────────────────────────────────────

    def list_applications(self, course_id: int, search: str | None, status: str | None, page: int, size: int):
        q = [CourseApplication.course_id == course_id]
        if search:
            q.append(
                CourseApplication.full_name.ilike(f"%{search}%") |
                CourseApplication.email.ilike(f"%{search}%")
            )
        if status:
            q.append(CourseApplication.status == status)
        stmt = select(CourseApplication).where(*q).order_by(CourseApplication.created_at.desc())
        items = list(self.db.scalars(stmt.offset((page - 1) * size).limit(size)))
        total = self.db.scalar(select(func.count()).select_from(CourseApplication).where(*q)) or 0
        return items, total

    def get_application(self, uuid: str) -> CourseApplication | None:
        return self.db.scalar(select(CourseApplication).where(CourseApplication.uuid == uuid))

    def create_application(self, course_id: int, data: dict) -> CourseApplication:
        app = CourseApplication(course_id=course_id, **data)
        self.db.add(app)
        self.db.commit()
        self.db.refresh(app)
        return app

    def save_application(self, app: CourseApplication, data: dict) -> CourseApplication:
        for k, v in data.items():
            setattr(app, k, v)
        self.db.commit()
        self.db.refresh(app)
        return app

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _slugify(self, title: str) -> str:
        slug = title.lower().strip()
        slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
        return slug or "course"

    def _unique_slug(self, title: str) -> str:
        base = self._slugify(title)
        slug = base
        counter = 1
        while self.db.scalar(select(func.count()).select_from(Course).where(Course.slug == slug)) > 0:
            slug = f"{base}-{counter}"
            counter += 1
        return slug
