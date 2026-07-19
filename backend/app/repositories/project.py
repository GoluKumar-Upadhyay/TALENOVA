"""Project persistence layer."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.project import Project
class ProjectRepository:
    """Database queries for project records."""
    def __init__(self, db: Session) -> None: self.db = db
    SORT_FIELDS = {"title": Project.title, "display_order": Project.display_order, "created_at": Project.created_at, "status": Project.status}
    def list(self, search: str | None, status: str | None, featured: bool | None, is_active: bool | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[Project], int]:
        """Return searchable non-deleted project records."""
        filters = [Project.is_deleted.is_(False)]
        if search: filters.append(Project.title.ilike(f"%{search}%"))
        if status: filters.append(Project.status == status)
        if featured is not None: filters.append(Project.is_featured == featured)
        if is_active is not None: filters.append(Project.is_active == is_active)
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query = select(Project).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page - 1) * page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(Project).where(*filters)) or 0
    def get(self, uuid: str) -> Project | None:
        """Get project by public id."""
        return self.db.scalar(select(Project).where(Project.uuid == uuid, Project.is_deleted.is_(False)))
    def create(self, values: dict) -> Project:
        """Persist project."""
        item = Project(**values); self.db.add(item); self.db.commit(); self.db.refresh(item); return item
    def save(self, item: Project, values: dict) -> Project:
        """Persist a project mutation."""
        for key, value in values.items(): setattr(item, key, value)
        self.db.commit(); self.db.refresh(item); return item
