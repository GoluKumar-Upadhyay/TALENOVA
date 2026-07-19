"""Hero section and statistic business operations."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.hero import HeroSection, Statistic
from app.repositories.hero import HeroRepository


class HeroService:
    """Coordinates hero section and statistic CRUD workflows."""

    HERO_SORT_FIELDS = set(HeroRepository.HERO_SORT_FIELDS)
    STAT_SORT_FIELDS = set(HeroRepository.STAT_SORT_FIELDS)

    def __init__(self, db: Session) -> None:
        self.repository = HeroRepository(db)

    def list_heroes(self, search, is_active, sort, direction, page, page_size):
        self._validate(sort, direction, self.HERO_SORT_FIELDS, "hero")
        return self.repository.list_heroes(search, is_active, sort, direction, page, page_size)

    def get_hero(self, uuid: str):
        item = self.repository.get_hero(uuid)
        if item is None:
            raise HTTPException(404, "Hero section not found")
        return item

    def create_hero(self, values: dict):
        return self.repository.save_hero(HeroSection(**values), {})

    def update_hero(self, uuid: str, values: dict):
        return self.repository.save_hero(self.get_hero(uuid), values)

    def delete_hero(self, uuid: str) -> None:
        self.repository.delete_hero(self.get_hero(uuid))

    def list_statistics(self, search, is_active, sort, direction, page, page_size):
        self._validate(sort, direction, self.STAT_SORT_FIELDS, "statistic")
        return self.repository.list_statistics(search, is_active, sort, direction, page, page_size)

    def get_statistic(self, uuid: str):
        item = self.repository.get_statistic(uuid)
        if item is None:
            raise HTTPException(404, "Statistic not found")
        return item

    def create_statistic(self, values: dict):
        return self.repository.save_statistic(Statistic(**values), {})

    def update_statistic(self, uuid: str, values: dict):
        return self.repository.save_statistic(self.get_statistic(uuid), values)

    def delete_statistic(self, uuid: str) -> None:
        self.repository.delete_statistic(self.get_statistic(uuid))

    def _validate(self, sort: str, direction: str, fields: set[str], label: str) -> None:
        if sort not in fields:
            raise HTTPException(422, f"Unsupported {label} sort field")
        if direction not in {"asc", "desc"}:
            raise HTTPException(422, "Unsupported sort direction")
