from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.course import CoursePage,CourseRead,CourseWrite
from app.services.course import CourseService
router=APIRouter(prefix="/courses",tags=["courses"])
@router.get("",response_model=CoursePage)
def list_courses(search:str|None=None,category_id:int|None=None,mentor_id:int|None=None,published:bool|None=None,coming_soon:bool|None=None,is_active:bool|None=None,sort:str=Query("display_order"),direction:str=Query("asc"),page:int=Query(1,ge=1),page_size:int=Query(24,ge=1,le=100),db:Session=Depends(get_db)):
 items,total=CourseService(db).list(search,category_id,mentor_id,published,coming_soon,is_active,sort,direction,page,page_size);return CoursePage(items=items,total=total,page=page,page_size=page_size)
@router.get("/{uuid}",response_model=CourseRead)
def get_course(uuid:str,db:Session=Depends(get_db)):return CourseService(db).get(uuid)
@router.post("",response_model=CourseRead,dependencies=[Depends(require("cms:write"))])
def create_course(data:CourseWrite,db:Session=Depends(get_db)):return CourseService(db).create(data.model_dump())
@router.put("/{uuid}",response_model=CourseRead,dependencies=[Depends(require("cms:write"))])
def update_course(uuid:str,data:CourseWrite,db:Session=Depends(get_db)):return CourseService(db).update(uuid,data.model_dump())
@router.delete("/{uuid}",dependencies=[Depends(require("cms:write"))])
def delete_course(uuid:str,db:Session=Depends(get_db)):CourseService(db).delete(uuid);return {"deleted":True}
