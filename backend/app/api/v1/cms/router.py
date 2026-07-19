from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.cms import ItemRead,ItemWrite,Page
from app.services.cms import CmsService
router=APIRouter(prefix="/cms",tags=["cms"])
@router.get("/{collection}",response_model=Page)
def list_items(collection:str,page:int=Query(1,ge=1),page_size:int=Query(24,ge=1,le=100),db:Session=Depends(get_db)):
    items,total=CmsService(db).list(collection,page,page_size);return Page(items=items,total=total,page=page,page_size=page_size)
@router.get("/{collection}/{uuid}",response_model=ItemRead)
def get_item(collection:str,uuid:str,db:Session=Depends(get_db)):
    item=CmsService(db).repo.get(uuid)
    if not item or item.collection != collection: raise HTTPException(404,"CMS item not found")
    return item
@router.post("/{collection}",response_model=ItemRead,dependencies=[Depends(require("cms:write"))])
def create_item(collection:str,data:ItemWrite,db:Session=Depends(get_db)):return CmsService(db).create(collection,data.model_dump(),None)
@router.put("/{uuid}",response_model=ItemRead,dependencies=[Depends(require("cms:write"))])
def update_item(uuid:str,data:ItemWrite,db:Session=Depends(get_db)):return CmsService(db).update(uuid,data.model_dump(),None)
@router.delete("/{uuid}",dependencies=[Depends(require("cms:write"))])
def delete_item(uuid:str,db:Session=Depends(get_db)):CmsService(db).delete(uuid,None);return {"deleted":True}
