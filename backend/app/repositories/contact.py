"""Contact message persistence."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.contact import ContactMessage
class ContactRepository:
    """Database access for student and college inquiries."""
    SORT_FIELDS = {"name": ContactMessage.name, "created_at": ContactMessage.created_at, "status": ContactMessage.status, "contact_type": ContactMessage.contact_type}
    def __init__(self, db: Session) -> None: self.db = db
    def list(self, contact_type: str | None, status: str | None, is_read: bool | None, archived: bool | None, search: str | None, sort: str, direction: str, page: int, page_size: int) -> tuple[list[ContactMessage], int]:
        filters = []
        if contact_type is not None: filters.append(ContactMessage.contact_type == contact_type)
        if status is not None: filters.append(ContactMessage.status == status)
        if is_read is not None: filters.append(ContactMessage.is_read == is_read)
        if archived is not None: filters.append(ContactMessage.is_archived == archived)
        if search:
            like=f"%{search}%";filters.append(ContactMessage.name.ilike(like)|ContactMessage.email.ilike(like)|ContactMessage.subject.ilike(like))
        order = self.SORT_FIELDS[sort].desc() if direction == "desc" else self.SORT_FIELDS[sort].asc()
        query=select(ContactMessage).where(*filters).order_by(order)
        return list(self.db.scalars(query.offset((page-1)*page_size).limit(page_size))), self.db.scalar(select(func.count()).select_from(ContactMessage).where(*filters)) or 0
    def create(self, values: dict) -> ContactMessage:
        item = ContactMessage(**values); self.db.add(item); self.db.commit(); self.db.refresh(item); return item
    def get(self, uuid: str) -> ContactMessage | None: return self.db.scalar(select(ContactMessage).where(ContactMessage.uuid == uuid))
    def save(self, item: ContactMessage, values: dict) -> ContactMessage:
        for key, value in values.items(): setattr(item, key, value)
        self.db.commit(); self.db.refresh(item); return item
