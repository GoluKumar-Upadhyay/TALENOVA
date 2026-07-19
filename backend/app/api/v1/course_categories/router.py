from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.course_category import CategoryPage,CourseCategoryRead,CourseCategoryWrite
from app.services.course_category import CourseCategoryService
router=APIRouter(prefix="/course-categories",tags=["course categories"])
@router.get("",response_model=CategoryPage)
def list_categories(search:str|None=None,page:int=Query(1,ge=1),page_size:int=Query(24,ge=1,le=100),db:Session=Depends(get_db)):
    items,total=CourseCategoryService(db).list(search,page,page_size);return CategoryPage(items=items,total=total,page=page,page_size=page_size)
@router.post("",response_model=CourseCategoryRead,dependencies=[Depends(require("cms:write"))])
def create_category(data:CourseCategoryWrite,db:Session=Depends(get_db)):return CourseCategoryService(db).create(data.model_dump())
@router.put("/{uuid}",response_model=CourseCategoryRead,dependencies=[Depends(require("cms:write"))])
def update_category(uuid:str,data:CourseCategoryWrite,db:Session=Depends(get_db)):return CourseCategoryService(db).update(uuid,data.model_dump())
@router.delete("/{uuid}",dependencies=[Depends(require("cms:write"))])
def delete_category(uuid:str,db:Session=Depends(get_db)):CourseCategoryService(db).delete(uuid);return {"deleted":True}
