from typing import Generic, TypeVar

from src.shared.base.repository import BaseRepository
from src.shared.exceptions.domain import NotFoundError

ModelT = TypeVar("ModelT")


class BaseService(Generic[ModelT]):
    def __init__(self, repository: BaseRepository[ModelT]) -> None:
        self.repository = repository

    async def get_by_id(self, entity_id: int) -> ModelT:
        entity = await self.repository.get_by_id(entity_id)
        if not entity:
            raise NotFoundError(f"Recurso con id {entity_id} no encontrado")
        return entity

    async def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[list[ModelT], int]:
        items = await self.repository.get_all(skip=skip, limit=limit)
        total = await self.repository.count()
        return items, total

    async def create(self, data: dict) -> ModelT:
        return await self.repository.create(data)

    async def update(self, entity_id: int, data: dict) -> ModelT:
        entity = await self.repository.update(entity_id, data)
        if not entity:
            raise NotFoundError(f"Recurso con id {entity_id} no encontrado")
        return entity

    async def delete(self, entity_id: int) -> None:
        deleted = await self.repository.delete(entity_id)
        if not deleted:
            raise NotFoundError(f"Recurso con id {entity_id} no encontrado")
