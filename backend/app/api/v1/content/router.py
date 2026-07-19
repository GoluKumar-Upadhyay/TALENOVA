from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.content import ContentRead,ContentWrite,ResultPage
from app.services.content import ContentService
router=APIRouter(prefix="/content",tags=["content"])
@router.get("/{module}",response_model=ResultPage)
def list_content(module:str,search:str|None=None,is_active:bool|None=None,sort:str=Query("display_order"),direction:str=Query("asc"),page:int=Query(1,ge=1),page_size:int=Query(24,ge=1,le=100),db:Session=Depends(get_db)):
    items,total=ContentService(db).list(module,search,is_active,sort,direction,page,page_size);return ResultPage(items=items,total=total,page=page,page_size=page_size)
@router.get("/{module}/{uuid}",response_model=ContentRead)
def get_content(module:str,uuid:str,db:Session=Depends(get_db)):
    item=ContentService(db).get(uuid)
    if not item or item.module != module: raise HTTPException(404,"Content not found")
    return item
@router.post("/{module}",response_model=ContentRead,dependencies=[Depends(require("cms:write"))])
def create_content(module:str,data:ContentWrite,db:Session=Depends(get_db)):return ContentService(db).create(module,data.model_dump())
@router.put("/{uuid}",response_model=ContentRead,dependencies=[Depends(require("cms:write"))])
def update_content(uuid:str,data:ContentWrite,db:Session=Depends(get_db)):return ContentService(db).update(uuid,data.model_dump())
@router.delete("/{uuid}",dependencies=[Depends(require("cms:write"))])
def delete_content(uuid:str,db:Session=Depends(get_db)):ContentService(db).delete(uuid);return {"deleted":True}
