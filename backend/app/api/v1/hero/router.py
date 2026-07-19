"""Hero and homepage statistic REST API."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.v1.auth.router import require
from app.db.session import get_db
from app.schemas.hero import HeroPage, HeroRead, HeroWrite, StatisticPage, StatisticRead, StatisticWrite
from app.services.hero import HeroService

router = APIRouter(prefix="/hero", tags=["hero"])


@router.get("", response_model=HeroPage)
def list_hero(search: str | None = None, is_active: bool | None = True, sort: str = Query("created_at"), direction: str = Query("desc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> HeroPage:
    items, total = HeroService(db).list_heroes(search, is_active, sort, direction, page, page_size)
    return HeroPage(items=items, total=total, page=page, page_size=page_size)


@router.post("", response_model=HeroRead, dependencies=[Depends(require("cms:write"))])
def create_hero(data: HeroWrite, db: Session = Depends(get_db)) -> HeroRead:
    return HeroService(db).create_hero(data.model_dump())


@router.get("/statistics", response_model=StatisticPage)
def list_stats(search: str | None = None, is_active: bool | None = True, sort: str = Query("display_order"), direction: str = Query("asc"), page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)) -> StatisticPage:
    items, total = HeroService(db).list_statistics(search, is_active, sort, direction, page, page_size)
    return StatisticPage(items=items, total=total, page=page, page_size=page_size)


@router.post("/statistics", response_model=StatisticRead, dependencies=[Depends(require("cms:write"))])
def create_stat(data: StatisticWrite, db: Session = Depends(get_db)) -> StatisticRead:
    return HeroService(db).create_statistic(data.model_dump())


@router.get("/statistics/{uuid}", response_model=StatisticRead)
def get_stat(uuid: str, db: Session = Depends(get_db)) -> StatisticRead:
    return HeroService(db).get_statistic(uuid)


@router.put("/statistics/{uuid}", response_model=StatisticRead, dependencies=[Depends(require("cms:write"))])
def update_stat(uuid: str, data: StatisticWrite, db: Session = Depends(get_db)) -> StatisticRead:
    return HeroService(db).update_statistic(uuid, data.model_dump())


@router.delete("/statistics/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_stat(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    HeroService(db).delete_statistic(uuid)
    return {"deleted": True}


@router.get("/{uuid}", response_model=HeroRead)
def get_hero(uuid: str, db: Session = Depends(get_db)) -> HeroRead:
    return HeroService(db).get_hero(uuid)


@router.put("/{uuid}", response_model=HeroRead, dependencies=[Depends(require("cms:write"))])
def update_hero(uuid: str, data: HeroWrite, db: Session = Depends(get_db)) -> HeroRead:
    return HeroService(db).update_hero(uuid, data.model_dump())


@router.delete("/{uuid}", dependencies=[Depends(require("cms:write"))])
def delete_hero(uuid: str, db: Session = Depends(get_db)) -> dict[str, bool]:
    HeroService(db).delete_hero(uuid)
    return {"deleted": True}
