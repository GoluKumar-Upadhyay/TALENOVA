"""Testimonial REST API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.testimonial import TestimonialPage, TestimonialRead, TestimonialWrite
from app.services.testimonial import TestimonialService
router = APIRouter(prefix="/testimonials", tags=["testimonials"])
@router.get("", response_model=TestimonialPage)
def list_testimonials(search: str | None = None, featured: bool | None = None, is_active: bool | None = None, min_rating: int | None = Query(None, ge=1, le=5), sort: str = Query("display_order"), direction: str = Query("asc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> TestimonialPage:
    """List testimonials."""
    items, total = TestimonialService(db).list(search, featured, is_active, min_rating, sort, direction, page, page_size)
    return TestimonialPage(items=items, total=total, page=page, page_size=page_size)
@router.get("/{uuid}", response_model=TestimonialRead)
def get_testimonial(uuid: str, db: Session = Depends(get_db)) -> TestimonialRead:
    """Get testimonial by id."""
    return TestimonialService(db).get(uuid)
@router.post("", response_model=TestimonialRead, dependencies=[Depends(require("cms:write"))])
def create_testimonial(data: TestimonialWrite, db: Session = Depends(get_db)) -> TestimonialRead:
    """Create testimonial after photo upload to Supabase Storage."""
    return TestimonialService(db).create(data.model_dump())
@router.put("/{uuid}", response_model=TestimonialRead, dependencies=[Depends(require("cms:write"))])
def update_testimonial(uuid: str, data: TestimonialWrite, db: Session = Depends(get_db)) -> TestimonialRead:
    """Update testimonial."""
    return TestimonialService(db).update(uuid, data.model_dump())
@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_testimonial(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    """Soft-delete testimonial."""
    TestimonialService(db).delete(uuid)
    return {"deleted": True}
